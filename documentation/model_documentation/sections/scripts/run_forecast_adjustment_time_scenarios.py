#!/usr/bin/env python3
"""
Forecast scenario analysis for Urban Expansion Adjustment Time.

Use:
    python run_forecast_adjustment_time_scenarios.py

Required files in the same folder:
    DiamondDuck_Forecast_v1_Calibrated.mdl

Outputs:
    results/forecast_adjustment_time_scenarios/
        scenario_timeseries.csv
        scenario_summary_key_years.csv
        scenario_2050_comparison.csv
        urban_land_scenarios.png
"""

from pathlib import Path
import math

import numpy as np
import pandas as pd
import pysd


MODEL_PATH = Path("DiamondDuck_Forecast_v1_Calibrated.mdl")
OUT_DIR = Path("results/forecast_adjustment_time_scenarios")
OUT_DIR.mkdir(parents=True, exist_ok=True)

YEARS = np.arange(2025, 2051)
KEY_YEARS = [2025, 2030, 2035, 2040, 2045, 2050]

# Scenario axis:
# Lower value = faster conversion of Urban Land Gap into actual land conversion.
# Higher value = slower / more constrained implementation.
ADJUSTMENT_TIME_SCENARIOS = {
    "fast_calibrated_3y": 3,
    "medium_fast_5y": 5,
    "medium_7y": 7,
    "original_10y": 10,
    "slow_15y": 15,
    "very_slow_20y": 20,
}

RETURN_COLUMNS_REAL = [
    "Urban Land",
    "Aggricultural Land",
    "Land Conversion Rate",
    "Urban Land Gap",
    "Expected Population",
    "Agricultural Scarcity Index",
    "Populational Need of Kcal in Km2",
    "Yield",
    "Mean Household Size",
    "Income per Capita",
    "Transport Cost per km",
    "Agricultural Rent",
]


def get_name_map(model) -> dict:
    """Map Vensim real names to PySD internal names."""
    doc = model.doc if not callable(model.doc) else model.doc()
    return dict(zip(doc["Real Name"], doc["Py Name"]))


def py_name(name_map: dict, real_name: str) -> str:
    return name_map.get(real_name, real_name)


def run_scenario(model, name_map: dict, scenario_name: str, adjustment_time: float) -> pd.DataFrame:
    """Run one forecast scenario."""
    params_real = {
        "Urban Expansion Adjustment Time": adjustment_time,
    }

    params_py = {
        py_name(name_map, real_name): value
        for real_name, value in params_real.items()
    }

    return_columns_py = [py_name(name_map, c) for c in RETURN_COLUMNS_REAL]

    result = model.run(
        params=params_py,
        return_columns=return_columns_py,
        return_timestamps=YEARS,
        reload=True,
    )

    result = result.reset_index()
    result = result.rename(columns={result.columns[0]: "Year"})

    rename_back = {
        py_name(name_map, c): c
        for c in RETURN_COLUMNS_REAL
    }
    result = result.rename(columns=rename_back)

    result["Scenario"] = scenario_name
    result["Urban Expansion Adjustment Time"] = adjustment_time

    return result


def add_summary_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Add interpretable forecast metrics."""
    df = df.copy()

    base_by_scenario = (
        df[df["Year"] == 2025]
        .set_index("Scenario")["Urban Land"]
        .to_dict()
    )

    df["Urban Land Increase since 2025"] = df.apply(
        lambda row: row["Urban Land"] - base_by_scenario[row["Scenario"]],
        axis=1,
    )

    df["Urban Land Growth Percent since 2025"] = df.apply(
        lambda row: 100 * (row["Urban Land"] / base_by_scenario[row["Scenario"]] - 1),
        axis=1,
    )

    return df


def make_plot(timeseries: pd.DataFrame) -> None:
    """Create a simple PNG plot. If matplotlib is unavailable, silently skip."""
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print("matplotlib not available, skipping plot.")
        return

    plt.figure(figsize=(10, 6))

    for scenario, sub in timeseries.groupby("Scenario"):
        plt.plot(sub["Year"], sub["Urban Land"], label=scenario)

    plt.xlabel("Year")
    plt.ylabel("Urban Land [km²]")
    plt.title("Urban Land forecast under different adjustment times")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_DIR / "urban_land_scenarios.png", dpi=200)
    plt.close()


def main() -> None:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH.resolve()}\n"
            "Place this script in the same folder as DiamondDuck_Forecast_v1_Calibrated.mdl."
        )

    print(f"Loading model: {MODEL_PATH}")
    model = pysd.read_vensim(str(MODEL_PATH))
    name_map = get_name_map(model)

    all_runs = []

    for scenario_name, adjustment_time in ADJUSTMENT_TIME_SCENARIOS.items():
        print(f"Running {scenario_name}: Urban Expansion Adjustment Time = {adjustment_time}")
        df = run_scenario(model, name_map, scenario_name, adjustment_time)
        all_runs.append(df)

    timeseries = pd.concat(all_runs, ignore_index=True)
    timeseries = add_summary_metrics(timeseries)

    summary_key_years = (
        timeseries[timeseries["Year"].isin(KEY_YEARS)]
        .sort_values(["Scenario", "Year"])
        .reset_index(drop=True)
    )

    comparison_2050 = (
        timeseries[timeseries["Year"] == 2050]
        [
            [
                "Scenario",
                "Urban Expansion Adjustment Time",
                "Urban Land",
                "Urban Land Increase since 2025",
                "Urban Land Growth Percent since 2025",
                "Aggricultural Land",
                "Land Conversion Rate",
                "Urban Land Gap",
            ]
        ]
        .sort_values("Urban Expansion Adjustment Time")
        .reset_index(drop=True)
    )

    timeseries.to_csv(OUT_DIR / "scenario_timeseries.csv", index=False)
    summary_key_years.to_csv(OUT_DIR / "scenario_summary_key_years.csv", index=False)
    comparison_2050.to_csv(OUT_DIR / "scenario_2050_comparison.csv", index=False)

    make_plot(timeseries)

    print("\n2050 comparison")
    print(comparison_2050.to_string(index=False))

    print(f"\nDone. Results written to: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
