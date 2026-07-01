from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import pysd
from scipy.optimize import differential_evolution

warnings.filterwarnings("ignore")

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------

MODEL_PATH = Path("model/DiamondDuck_Backtesting_Option1_UrbanLand.mdl")
if not MODEL_PATH.exists():
    MODEL_PATH = Path("DiamondDuck_Backtesting_Option1_UrbanLand.mdl")

OUT_DIR = Path("results/backtesting_calibration_v2")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------
# Backtesting setup
# -------------------------------------------------------------------

YEARS = np.arange(2000, 2026)
CALIBRATION_YEARS = YEARS

RETURN_COLUMNS_REAL = [
    "Urban Land",
    "Historical Urban Land",
    "Urban Land Error Percent",
    "Urban Land Absolute Error Percent",
]

# Stage 1: minimal, clean tuning
PARAM_BOUNDS_STAGE_1 = {
    "Urban Expansion Adjustment Time": (3, 20),
}

# Stage 2: use only if Stage 1 cannot fit history well enough
# This parameter is data-adjacent and should stay narrow.
PARAM_BOUNDS_STAGE_2 = {
    "Urban Expansion Adjustment Time": (3, 20),
    "Reference Initial Land Demand per Capita": (0.00036, 0.00044),
}

STAGES = {
    "stage_1_adjustment_time_only": PARAM_BOUNDS_STAGE_1,
    "stage_2_adjustment_time_plus_land_demand": PARAM_BOUNDS_STAGE_2,
}

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

print(f"Loading model: {MODEL_PATH}")
model = pysd.read_vensim(str(MODEL_PATH))
model_doc = model.doc if not callable(model.doc) else model.doc()
name_map = dict(zip(model_doc["Real Name"], model_doc["Py Name"]))


def py_name(real_name: str) -> str:
    return name_map.get(real_name, real_name)


RETURN_COLUMNS_PY = [py_name(name) for name in RETURN_COLUMNS_REAL]


def convert_params_to_pysd(params_real: dict) -> dict:
    return {py_name(k): v for k, v in params_real.items()}


def vector_to_params(x: np.ndarray, bounds: dict) -> dict:
    return {name: float(value) for name, value in zip(bounds.keys(), x)}


def run_model(params_real: dict | None = None, years=YEARS) -> pd.DataFrame:
    params_real = params_real or {}
    result = model.run(
        params=convert_params_to_pysd(params_real),
        return_columns=RETURN_COLUMNS_PY,
        return_timestamps=years,
        reload=True,
    )
    result = result.reset_index().rename(columns={result.index.name or result.columns[0]: "Year"})
    if "index" in result.columns:
        result = result.rename(columns={"index": "Year"})

    rename_back = {py_name(real): real for real in RETURN_COLUMNS_REAL}
    result = result.rename(columns=rename_back)
    return result


def calculate_scores(df: pd.DataFrame, years=CALIBRATION_YEARS) -> dict:
    sub = df[df["Year"].isin(years)].copy()
    err = sub["Urban Land Error Percent"].astype(float)
    abs_err = err.abs()
    return {
        "RMSE Error Percent": float(np.sqrt(np.mean(err ** 2))),
        "MAE Error Percent": float(np.mean(abs_err)),
        "Max Absolute Error Percent": float(np.max(abs_err)),
        "Mean Error Percent": float(np.mean(err)),
        "Final Year Error Percent": float(err.iloc[-1]),
    }


def calibrate_stage(stage_name: str, bounds: dict) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    print(f"\nRunning {stage_name}")
    history = []

    def objective(x: np.ndarray) -> float:
        params = vector_to_params(x, bounds)
        try:
            df = run_model(params)
            scores = calculate_scores(df)
            score = scores["RMSE Error Percent"]
            if not np.isfinite(score):
                return 1e12
            history.append({"Stage": stage_name, "Score Train RMSE Percent": score, **params, **scores})
            return score
        except Exception as exc:
            history.append({"Stage": stage_name, "Score Train RMSE Percent": 1e12, "Error": str(exc), **params})
            return 1e12

    result = differential_evolution(
        objective,
        bounds=list(bounds.values()),
        maxiter=50,
        popsize=10,
        seed=42,
        polish=True,
        workers=1,
        updating="immediate",
    )

    best_params = vector_to_params(result.x, bounds)
    best_df = run_model(best_params)
    best_scores = calculate_scores(best_df)

    runs_df = pd.DataFrame(history).sort_values("Score Train RMSE Percent").reset_index(drop=True)
    params_df = pd.DataFrame({
        "Stage": stage_name,
        "Parameter": list(best_params.keys()),
        "Best Value": list(best_params.values()),
        "Lower Bound": [v[0] for v in bounds.values()],
        "Upper Bound": [v[1] for v in bounds.values()],
    })
    scores_df = pd.DataFrame([{ "Stage": stage_name, **best_scores }])

    return best_df, params_df, scores_df, runs_df


# -------------------------------------------------------------------
# Main run
# -------------------------------------------------------------------

baseline_df = run_model()
baseline_scores = calculate_scores(baseline_df)
baseline_scores_df = pd.DataFrame([{ "Stage": "baseline", **baseline_scores }])
print("\nBaseline scores")
print(baseline_scores_df.to_string(index=False))

all_best = []
all_params = []
all_scores = [baseline_scores_df]
all_runs = []

for stage_name, bounds in STAGES.items():
    best_df, params_df, scores_df, runs_df = calibrate_stage(stage_name, bounds)
    best_df["Stage"] = stage_name
    all_best.append(best_df)
    all_params.append(params_df)
    all_scores.append(scores_df)
    all_runs.append(runs_df)
    print(scores_df.to_string(index=False))
    print(params_df.to_string(index=False))

best_timeseries_df = pd.concat(all_best, ignore_index=True)
best_params_df = pd.concat(all_params, ignore_index=True)
score_summary_df = pd.concat(all_scores, ignore_index=True)
runs_df = pd.concat(all_runs, ignore_index=True).sort_values("Score Train RMSE Percent").reset_index(drop=True)

baseline_export = baseline_df.rename(columns={
    "Urban Land": "Baseline Urban Land",
    "Urban Land Error Percent": "Baseline Error Percent",
    "Urban Land Absolute Error Percent": "Baseline Absolute Error Percent",
})

# Export
baseline_df.to_csv(OUT_DIR / "baseline_timeseries.csv", index=False)
best_timeseries_df.to_csv(OUT_DIR / "calibrated_timeseries_by_stage.csv", index=False)
best_params_df.to_csv(OUT_DIR / "best_parameters_by_stage.csv", index=False)
score_summary_df.to_csv(OUT_DIR / "score_summary.csv", index=False)
runs_df.to_csv(OUT_DIR / "all_calibration_runs.csv", index=False)

with pd.ExcelWriter(OUT_DIR / "calibration_summary.xlsx") as writer:
    score_summary_df.to_excel(writer, sheet_name="Scores", index=False)
    best_params_df.to_excel(writer, sheet_name="Best Parameters", index=False)
    best_timeseries_df.to_excel(writer, sheet_name="Time Series", index=False)
    runs_df.head(200).to_excel(writer, sheet_name="Top Runs", index=False)

print(f"\nDone. Results written to: {OUT_DIR.resolve()}")
print("\nScore summary")
print(score_summary_df.to_string(index=False))
