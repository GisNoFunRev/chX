#!/usr/bin/env python3
"""
Backtesting driver diagnostics.

Goal:
Find why Urban Land grows slowly at first and then rises more strongly.

Use:
    python diagnose_backtesting_dynamics.py

Required file in the same folder:
    DiamondDuck_Backtesting_Option1_UrbanLand.mdl

Outputs:
    results/backtesting_diagnostics/
        diagnostic_timeseries.csv
        phase_summary.csv
        driver_correlations.csv
        bottleneck_flags.csv
        available_model_variables.csv
        urban_land_diagnostics.png  optional, if matplotlib is installed
"""

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import pysd


MODEL_PATH = Path("DiamondDuck_Backtesting_Option1_UrbanLand.mdl")
OUT_DIR = Path("results/backtesting_diagnostics")
OUT_DIR.mkdir(parents=True, exist_ok=True)

YEARS = np.arange(2000, 2026)

# Variables likely to explain the late acceleration.
# Missing variables are skipped automatically.
REQUESTED_VARIABLES_REAL = [
    "Urban Land",
    "Historical Urban Land",
    "Urban Land Error Percent",
    "Urban Land Absolute Error Percent",

    "Land Conversion Rate",
    "Urban Land Gap",
    "Desired Urban Land Total",
    "Desired Urban Land",
    "AMM Consistent Economic Land Conversion Demand",
    "Land Conversion Pressure Factors",
    "Max Feasible Conversion",

    "Expected Population",
    "Number of Households",
    "Mean Household Size",
    "Income per Capita",
    "Mean Household Income",
    "Transport Cost per km",
    "Agricultural Rent",

    "Urban Fringe Radius",
    "Land Demand per Household q",
    "Reference Initial Land Demand per Capita",
    "Housing Preference Share Alpha",

    "Agricultural Scarcity Index",
    "Populational Need of Kcal in Km2",
    "Yield",
    "Innovation Index",
    "Urban Productivity Effect",
]


def get_doc(model) -> pd.DataFrame:
    doc = model.doc if not callable(model.doc) else model.doc()
    return doc.copy()


def get_name_map(doc: pd.DataFrame) -> dict:
    return dict(zip(doc["Real Name"], doc["Py Name"]))


def py_name(name_map: dict, real_name: str) -> str:
    return name_map.get(real_name, real_name)


def available_real_names(doc: pd.DataFrame) -> set:
    return set(doc["Real Name"].astype(str))


def run_model(model, doc: pd.DataFrame) -> pd.DataFrame:
    names = available_real_names(doc)
    missing = [v for v in REQUESTED_VARIABLES_REAL if v not in names]
    present = [v for v in REQUESTED_VARIABLES_REAL if v in names]

    if missing:
        print("Skipped missing variables:")
        for v in missing:
            print(f"  - {v}")

    name_map = get_name_map(doc)
    return_columns_py = [py_name(name_map, v) for v in present]

    result = model.run(
        return_columns=return_columns_py,
        return_timestamps=YEARS,
        reload=True,
    )

    result = result.reset_index()
    result = result.rename(columns={result.columns[0]: "Year"})

    rename_back = {py_name(name_map, v): v for v in present}
    result = result.rename(columns=rename_back)

    return result


def add_diagnostics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "Urban Land" in df:
        df["Urban Land annual change"] = df["Urban Land"].diff()
        df["Urban Land annual acceleration"] = df["Urban Land annual change"].diff()

    if "Historical Urban Land" in df:
        df["Historical Urban Land annual change"] = df["Historical Urban Land"].diff()

    if {"Urban Land", "Historical Urban Land"}.issubset(df.columns):
        df["Urban Land absolute gap to historical"] = df["Urban Land"] - df["Historical Urban Land"]

    if {"Land Conversion Rate", "Urban Land Gap"}.issubset(df.columns):
        df["Conversion per Gap"] = np.where(
            df["Urban Land Gap"].abs() > 1e-9,
            df["Land Conversion Rate"] / df["Urban Land Gap"],
            np.nan,
        )

    if {"Land Conversion Rate", "AMM Consistent Economic Land Conversion Demand"}.issubset(df.columns):
        df["LCR / AMM demand"] = np.where(
            df["AMM Consistent Economic Land Conversion Demand"].abs() > 1e-9,
            df["Land Conversion Rate"] / df["AMM Consistent Economic Land Conversion Demand"],
            np.nan,
        )

    if {"Land Conversion Rate", "Max Feasible Conversion"}.issubset(df.columns):
        df["LCR / Max Feasible Conversion"] = np.where(
            df["Max Feasible Conversion"].abs() > 1e-9,
            df["Land Conversion Rate"] / df["Max Feasible Conversion"],
            np.nan,
        )
        df["Near max feasible cap"] = df["LCR / Max Feasible Conversion"] > 0.95

    if {"AMM Consistent Economic Land Conversion Demand", "Max Feasible Conversion"}.issubset(df.columns):
        df["Demand exceeds feasible cap"] = (
            df["AMM Consistent Economic Land Conversion Demand"] > df["Max Feasible Conversion"]
        )

    # Identify the biggest acceleration year.
    if "Urban Land annual acceleration" in df:
        valid = df.dropna(subset=["Urban Land annual acceleration"])
        if not valid.empty:
            max_idx = valid["Urban Land annual acceleration"].idxmax()
            df["Largest acceleration year flag"] = False
            df.loc[max_idx, "Largest acceleration year flag"] = True

    return df


def make_phase_summary(df: pd.DataFrame) -> pd.DataFrame:
    periods = [
        ("early_2000_2006", 2000, 2006),
        ("middle_2006_2012", 2006, 2012),
        ("late_2012_2018", 2012, 2018),
        ("post_2018_2025", 2018, 2025),
        ("full_2000_2025", 2000, 2025),
    ]

    rows = []
    for label, start, end in periods:
        sub = df[(df["Year"] >= start) & (df["Year"] <= end)].copy()
        row = {"period": label, "start": start, "end": end}

        for col in [
            "Urban Land",
            "Historical Urban Land",
            "Land Conversion Rate",
            "Urban Land Gap",
            "Desired Urban Land Total",
            "AMM Consistent Economic Land Conversion Demand",
            "Max Feasible Conversion",
            "Income per Capita",
            "Mean Household Size",
            "Agricultural Rent",
            "Agricultural Scarcity Index",
        ]:
            if col in sub.columns:
                row[f"{col} start"] = float(sub.iloc[0][col])
                row[f"{col} end"] = float(sub.iloc[-1][col])
                row[f"{col} change"] = float(sub.iloc[-1][col] - sub.iloc[0][col])
                row[f"{col} mean"] = float(sub[col].mean())

        if "Urban Land annual change" in sub.columns:
            row["Mean annual Urban Land change"] = float(sub["Urban Land annual change"].mean(skipna=True))
            row["Max annual Urban Land change"] = float(sub["Urban Land annual change"].max(skipna=True))

        if "Urban Land Error Percent" in sub.columns:
            row["Mean Urban Land Error Percent"] = float(sub["Urban Land Error Percent"].mean())

        rows.append(row)

    return pd.DataFrame(rows)


def make_driver_correlations(df: pd.DataFrame) -> pd.DataFrame:
    target = "Urban Land annual change"
    if target not in df.columns:
        return pd.DataFrame()

    candidate_cols = [
        "Land Conversion Rate",
        "Urban Land Gap",
        "Desired Urban Land Total",
        "Desired Urban Land",
        "AMM Consistent Economic Land Conversion Demand",
        "Land Conversion Pressure Factors",
        "Max Feasible Conversion",
        "Expected Population",
        "Number of Households",
        "Mean Household Size",
        "Income per Capita",
        "Mean Household Income",
        "Transport Cost per km",
        "Agricultural Rent",
        "Urban Fringe Radius",
        "Land Demand per Household q",
        "Agricultural Scarcity Index",
        "Yield",
        "Innovation Index",
        "Urban Productivity Effect",
    ]

    rows = []
    sub = df.dropna(subset=[target]).copy()

    for col in candidate_cols:
        if col in sub.columns:
            x = sub[col].astype(float)
            y = sub[target].astype(float)
            if x.nunique(dropna=True) > 1 and y.nunique(dropna=True) > 1:
                rows.append({
                    "driver": col,
                    "correlation_with_urban_land_annual_change": float(x.corr(y)),
                    "driver_change_2000_2025": float(df[col].iloc[-1] - df[col].iloc[0]),
                    "driver_start": float(df[col].iloc[0]),
                    "driver_end": float(df[col].iloc[-1]),
                })

    return (
        pd.DataFrame(rows)
        .sort_values("correlation_with_urban_land_annual_change", ascending=False)
        .reset_index(drop=True)
    )


def make_bottleneck_flags(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["Year"]

    for col in [
        "Land Conversion Rate",
        "Urban Land Gap",
        "AMM Consistent Economic Land Conversion Demand",
        "Max Feasible Conversion",
        "LCR / AMM demand",
        "LCR / Max Feasible Conversion",
        "Near max feasible cap",
        "Demand exceeds feasible cap",
        "Conversion per Gap",
        "Largest acceleration year flag",
    ]:
        if col in df.columns:
            cols.append(col)

    return df[cols].copy()


def make_plot(df: pd.DataFrame) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print("matplotlib not available, skipping plot.")
        return

    plot_cols = [c for c in [
        "Urban Land",
        "Historical Urban Land",
        "Land Conversion Rate",
        "Urban Land Gap",
        "Desired Urban Land Total",
    ] if c in df.columns]

    for col in plot_cols:
        plt.figure(figsize=(9, 5))
        plt.plot(df["Year"], df[col])
        plt.xlabel("Year")
        plt.ylabel(col)
        plt.title(col)
        plt.tight_layout()
        safe = col.lower().replace(" ", "_").replace("/", "_")
        plt.savefig(OUT_DIR / f"{safe}.png", dpi=180)
        plt.close()


def main() -> None:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH.resolve()}\n"
            "Place this script in the same folder as DiamondDuck_Backtesting_Option1_UrbanLand.mdl."
        )

    print(f"Loading model: {MODEL_PATH}")
    model = pysd.read_vensim(str(MODEL_PATH))
    doc = get_doc(model)

    doc.to_csv(OUT_DIR / "available_model_variables.csv", index=False)

    df = run_model(model, doc)
    df = add_diagnostics(df)

    phase_summary = make_phase_summary(df)
    correlations = make_driver_correlations(df)
    bottleneck_flags = make_bottleneck_flags(df)

    df.to_csv(OUT_DIR / "diagnostic_timeseries.csv", index=False)
    phase_summary.to_csv(OUT_DIR / "phase_summary.csv", index=False)
    correlations.to_csv(OUT_DIR / "driver_correlations.csv", index=False)
    bottleneck_flags.to_csv(OUT_DIR / "bottleneck_flags.csv", index=False)

    make_plot(df)

    print("\nPhase summary")
    keep = [c for c in [
        "period",
        "Urban Land change",
        "Mean annual Urban Land change",
        "Land Conversion Rate mean",
        "Urban Land Gap mean",
        "Desired Urban Land Total change",
        "Income per Capita change",
        "Agricultural Rent change",
    ] if c in phase_summary.columns]
    print(phase_summary[keep].to_string(index=False))

    print("\nTop driver correlations with annual Urban Land change")
    if not correlations.empty:
        print(correlations.head(10).to_string(index=False))
    else:
        print("No correlations computed.")

    print(f"\nDone. Results written to: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
