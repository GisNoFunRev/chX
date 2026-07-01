from pathlib import Path
import numpy as np
import pandas as pd
import pysd

MODEL_PATH = Path("DiamondDuck_Forecast_v1_Calibrated.mdl")
OUT_DIR = Path("results/forecast_v1")
OUT_DIR.mkdir(parents=True, exist_ok=True)

YEARS = np.arange(2025, 2051)
DISPLAY_YEARS = [2025, 2030, 2035, 2040, 2045, 2050]

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


def build_name_map(model):
    doc = model.doc if not callable(model.doc) else model.doc()
    return dict(zip(doc["Real Name"], doc["Py Name"]))


def py_name(name_map, real_name):
    return name_map.get(real_name, real_name)


def run_forecast():
    print(f"Loading model: {MODEL_PATH}")
    model = pysd.read_vensim(str(MODEL_PATH))
    name_map = build_name_map(model)
    return_columns_py = [py_name(name_map, c) for c in RETURN_COLUMNS_REAL]

    result = model.run(
        return_columns=return_columns_py,
        return_timestamps=YEARS,
        reload=True,
    )

    result = result.reset_index().rename(columns={result.columns[0]: "Year"})
    rename_back = {py_name(name_map, c): c for c in RETURN_COLUMNS_REAL}
    result = result.rename(columns=rename_back)
    return result


def main():
    df = run_forecast()
    df.to_csv(OUT_DIR / "forecast_timeseries.csv", index=False)

    summary = df[df["Year"].isin(DISPLAY_YEARS)].copy()
    summary.to_csv(OUT_DIR / "forecast_summary_5y.csv", index=False)

    with pd.ExcelWriter(OUT_DIR / "forecast_v1_summary.xlsx") as writer:
        summary.to_excel(writer, sheet_name="Summary 5y", index=False)
        df.to_excel(writer, sheet_name="Full Time Series", index=False)

    print("\nForecast summary")
    print(summary.to_string(index=False))
    print(f"\nDone. Results written to: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
