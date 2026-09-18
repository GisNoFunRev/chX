#!/usr/bin/env python3
"""
Empirical Land-Take Scenario for the forecast model.

Idea:
The model's internal Land Conversion Rate can be much higher than empirical
EEA-style land-take rates. This script runs forecast scenarios where actual
Land Conversion Rate is capped by an empirical annual land-take ceiling.

Use:
    python run_forecast_empirical_land_take_scenarios.py

Required file in the same folder:
    DiamondDuck_Forecast_v1_Calibrated.mdl

Outputs:
    results/forecast_empirical_land_take_scenarios/
        empirical_land_take_timeseries.csv
        empirical_land_take_key_years.csv
        empirical_land_take_2050_comparison.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pysd


MODEL_PATH = Path("DiamondDuck_Forecast_v1_Calibrated.mdl")
OUT_DIR = Path("results/forecast_empirical_land_take_scenarios")
OUT_DIR.mkdir(parents=True, exist_ok=True)

YEARS = np.arange(2025, 2051)
KEY_YEARS = [2025, 2030, 2035, 2040, 2045, 2050]

# Empirical land-take caps in km2/year.
# The labels describe how the scenario should be interpreted.
LAND_TAKE_CAP_SCENARIOS = {
    "eea_low_410_km2_per_year": 410,
    "empirical_mid_500_km2_per_year": 500,
    "eea_recent_540_km2_per_year": 540,
    "empirical_high_600_km2_per_year": 600,
    "uncapped_internal_model": None,
}

RETURN_COLUMNS_REAL = [
    "Urban Land",
    "Aggricultural Land",
    "Land Conversion Rate",
    "Urban Land Gap",
    "Expected Population",
    "Agricultural Scarcity Index",
    "Mean Household Size",
    "Income per Capita",
    "Transport Cost per km",
    "Agricultural Rent",
    "Max Feasible Conversion",
    "AMM Consistent Economic Land Conversion Demand",
    "Land Conversion Pressure Factors",
]


def get_name_map(model) -> dict:
    doc = model.doc if not callable(model.doc) else model.doc()
    return dict(zip(doc["Real Name"], doc["Py Name"]))


def py_name(name_map: dict, real_name: str) -> str:
    return name_map.get(real_name, real_name)


def run_scenario(model, name_map: dict, scenario_name: str, cap_value):
    params_real = {}

    # This works because Land Conversion Rate is defined as:
    # MIN(Land Conversion Pressure Factors, Max Feasible Conversion)
    # Overriding Max Feasible Conversion imposes an empirical annual cap.
    if cap_value is not None:
        params_real["Max Feasible Conversion"] = cap_value

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
    result["Empirical Land Take Cap km2 per year"] = cap_value if cap_value is not None else np.nan

    base_urban_land = float(result.loc[result["Year"] == 2025, "Urban Land"].iloc[0])
    result["Urban Land Increase since 2025"] = result["Urban Land"] - base_urban_land
    result["Urban Land Growth Percent since 2025"] = 100 * (result["Urban Land"] / base_urban_land - 1)

    return result


def main():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH.resolve()}\n"
            "Place this script in the same folder as DiamondDuck_Forecast_v1_Calibrated.mdl."
        )

    print(f"Loading model: {MODEL_PATH}")
    model = pysd.read_vensim(str(MODEL_PATH))
    name_map = get_name_map(model)

    all_runs = []

    for scenario_name, cap_value in LAND_TAKE_CAP_SCENARIOS.items():
        print(f"Running {scenario_name}: cap = {cap_value}")
        df = run_scenario(model, name_map, scenario_name, cap_value)
        all_runs.append(df)

    timeseries = pd.concat(all_runs, ignore_index=True)

    key_years = (
        timeseries[timeseries["Year"].isin(KEY_YEARS)]
        .sort_values(["Scenario", "Year"])
        .reset_index(drop=True)
    )

    comparison_2050 = (
        timeseries[timeseries["Year"] == 2050]
        [
            [
                "Scenario",
                "Empirical Land Take Cap km2 per year",
                "Urban Land",
                "Urban Land Increase since 2025",
                "Urban Land Growth Percent since 2025",
                "Aggricultural Land",
                "Land Conversion Rate",
                "Urban Land Gap",
                "Max Feasible Conversion",
            ]
        ]
        .sort_values("Urban Land")
        .reset_index(drop=True)
    )

    timeseries.to_csv(OUT_DIR / "empirical_land_take_timeseries.csv", index=False)
    key_years.to_csv(OUT_DIR / "empirical_land_take_key_years.csv", index=False)
    comparison_2050.to_csv(OUT_DIR / "empirical_land_take_2050_comparison.csv", index=False)

    print("\n2050 comparison")
    print(comparison_2050.to_string(index=False))

    print(f"\nDone. Results written to: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
