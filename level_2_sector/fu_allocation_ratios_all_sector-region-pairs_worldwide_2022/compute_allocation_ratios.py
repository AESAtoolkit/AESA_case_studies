"""Compute FU allocation ratios."""

from pathlib import Path
from typing import cast

import numpy as np
import pandas as pd

from pyaesa import (
    deterministic_asocc,
    download_mrio,
    download_pop_gdp,
    process_mrio,
    process_pop_gdp,
    set_workspace,
)

# ========
# Settings
# ========
# Replace this placeholder with the pyaesa workspace to use for the study.
WORKSPACE_PATH = Path("/path/to/pyaesa_workspace")

# Root name used for the deterministic aSoCC projects and ratio output folder.
PROJECT_NAME_ROOT = "uncasext_fu_ratio"

# Shared pyaesa selectors used by both MRIO processing and aSoCC runs.
SOURCE = "exiobase_3102_ixi"
YEAR = 2022
REFERENCE_YEAR = 1995
LCIA_METHOD = "gwp100_lcia"
IMPACT = "GWP_100"
AGG_SEC = True
AGG_VERSION = "elec"

# Output folder for the ratio CSVs.
RATIO_CSV_DIR = WORKSPACE_PATH / f"{PROJECT_NAME_ROOT}__ratio" / "csv"


# ===================
# Ratios computation
# ===================

RATIO_SPECS = [
    (
        "L2.c.a",
        "AR(E^{CBA_FD})",
        "L2.c.b",
        "AR(E^{CBA_TD})",
    ),
    (
        "L2.c.a",
        "AR(E^{CBA_FD})_UT(FD)",
        "L2.c.b",
        "AR(E^{CBA_FD})_UT(FDa)",
    ),
    (
        "L2.c.a",
        "EG(Pop)_UT(FD)",
        "L2.c.b",
        "EG(Pop)_UT(FDa)",
    ),
    (
        "L2.c.a",
        "PR(GDPcap)_UT(FD)",
        "L2.c.b",
        "PR(GDPcap)_UT(FDa)",
    ),
    (
        "L2.c.a",
        "PR-HR(Ecap,cum^{CBA_FD})_UT(FD)",
        "L2.c.b",
        "PR-HR(Ecap,cum^{CBA_FD})_UT(FDa)",
    ),
    (
        "L2.c.a",
        "UT(FD)",
        "L2.c.b",
        "UT(TD)",
    ),
    (
        "L2.a.c",
        "AR(E^{PBA})",
        "L2.c.b",
        "AR(E^{CBA_TD})",
    ),
    (
        "L2.a.c",
        "AR(E^{PBA})_UT(GVA)",
        "L2.c.b",
        "AR(E^{PBA})_UT(GVAa)",
    ),
    (
        "L2.a.c",
        "EG(Pop)_UT(GVA)",
        "L2.c.b",
        "EG(Pop)_UT(GVAa)",
    ),
    (
        "L2.a.c",
        "PR(GDPcap)_UT(GVA)",
        "L2.c.b",
        "PR(GDPcap)_UT(GVAa)",
    ),
    (
        "L2.a.c",
        "PR-HR(Ecap,cum^{PBA})_UT(GVA)",
        "L2.c.b",
        "PR-HR(Ecap,cum^{PBA})_UT(GVAa)",
    ),
    (
        "L2.a.c",
        "UT(GVA)",
        "L2.c.b",
        "UT(TD)",
    ),
]

COMBINED_FU_RATIO = "L2.c.a and L2.a.c / L2.c.b"


set_workspace(WORKSPACE_PATH)

download_pop_gdp()
process_pop_gdp()

download_mrio(SOURCE)
process_mrio(
    source=SOURCE,
    lcia_method=LCIA_METHOD,
    agg_sec=AGG_SEC,
    agg_version=AGG_VERSION,
)

fu_codes = sorted({spec[0] for spec in RATIO_SPECS} | {spec[2] for spec in RATIO_SPECS})
# Run deterministic aSoCC for every L2 FU required by the ratio specification.
asocc_roots: dict[str, Path] = {}
for fu_to_run in fu_codes:
    project_name = f"{PROJECT_NAME_ROOT}__{SOURCE}__{fu_to_run.replace('.', '_')}"
    report = deterministic_asocc(
        project_name=project_name,
        source=SOURCE,
        years=YEAR,
        fu_code=fu_to_run,
        agg_sec=AGG_SEC,
        agg_version=AGG_VERSION,
        lcia_method=LCIA_METHOD,
        reference_years=REFERENCE_YEAR,
        figures=False,
    )
    asocc_roots[fu_to_run] = cast(Path, report.output_root)


def format_ratio_label(num_fu, num_method, den_fu, den_method):
    """Return the readable FU/method ratio label."""
    return f"{num_fu}: {num_method} / {den_fu}: {den_method}"


def l2_rows(output_root, fu):
    """Read pyaesa L2 result CSVs and normalize the country and sector axes."""
    region_column = {"L2.a.c": "r_p", "L2.c.a": "r_f", "L2.c.b": "r_c"}[fu]
    rows = []
    for csv_path in sorted((output_root / "results" / "l2" / "l2_vs_global").glob("*.csv")):
        frame = pd.read_csv(csv_path)
        if "impact" in frame:
            frame = frame.loc[frame["impact"].eq(IMPACT)]
        if "reference_year" in frame:
            frame = frame.loc[frame["reference_year"].eq(REFERENCE_YEAR)]
        rows.append(
            pd.DataFrame(
                {
                    "fu_code": fu,
                    "method": frame["l1_l2_method"].astype(str).str.strip(),
                    "sector": frame["s_p"].astype(str).str.strip(),
                    "country": frame[region_column].astype(str).str.strip(),
                    "year": YEAR,
                    "value": pd.to_numeric(frame[str(YEAR)], errors="coerce"),
                }
            )
        )
    return pd.concat(rows, ignore_index=True)


def method_values(compiled, fu, method):
    """Return one indexed vector of aSoCC values for one FU and allocation method."""
    rows = compiled.loc[
        compiled["fu_code"].eq(fu) & compiled["method"].eq(method),
        ["sector", "country", "year", "value"],
    ]
    return rows.groupby(["sector", "country", "year"], dropna=False)["value"].sum(min_count=1)


def ratio_values(num, den):
    """Return FU ratios."""
    numerator = np.asarray(pd.to_numeric(num, errors="coerce"), dtype=float)
    denominator = np.asarray(pd.to_numeric(den, errors="coerce"), dtype=float)
    ratio = np.full(numerator.shape, np.nan)
    np.divide(numerator, denominator, out=ratio, where=denominator != 0)
    ratio[(numerator == 0) & (denominator > 0)] = 0
    ratio[(denominator == 0) & (numerator > 0)] = np.inf
    ratio[(denominator == 0) & (numerator == 0)] = 1
    return ratio


def build_distribution(compiled):
    """Compute ratio table from pyaesa aSoCC outputs."""
    ratio_frames = []
    for num_fu, num_method, den_fu, den_method in RATIO_SPECS:
        fu_ratio = f"{num_fu} / {den_fu}"
        label = format_ratio_label(num_fu, num_method, den_fu, den_method)
        numerator = method_values(compiled, num_fu, num_method)
        denominator = method_values(compiled, den_fu, den_method)
        merged = pd.concat([numerator, denominator], axis=1, keys=["num", "den"]).reset_index()
        ratio = ratio_values(merged["num"], merged["den"])

        frame = merged[["sector", "country", "year"]].copy()
        frame.insert(0, "display_label", label.replace(" / ", "\n"))
        frame.insert(0, "denominator_method", den_method)
        frame.insert(0, "denominator_fu", den_fu)
        frame.insert(0, "numerator_method", num_method)
        frame.insert(0, "numerator_fu", num_fu)
        frame.insert(0, "ratio_label", label)
        frame.insert(0, "fu_ratio", fu_ratio)
        frame["num"] = merged["num"].to_numpy()
        frame["den"] = merged["den"].to_numpy()
        frame["ratio"] = ratio
        frame["is_num_zero_den_positive"] = (frame["num"] == 0) & (frame["den"] > 0)
        frame["plot_ratio"] = np.where((ratio > 0) & np.isfinite(ratio), ratio, np.nan)
        ratio_frames.append(frame)

    return pd.concat(ratio_frames, ignore_index=True)


def summary_row(frame, summary_level, fu_ratio, allocation_ratio_label=""):
    """Return counts, mean, and quantiles."""
    values = np.asarray(pd.to_numeric(frame["plot_ratio"], errors="coerce"), dtype=float)
    values = values[np.isfinite(values) & (values > 0)]
    row = {
        "summary_level": summary_level,
        "fu_ratio": fu_ratio,
        "ratio_label": allocation_ratio_label,
        "row_count": len(frame),
        "ratio_count": len(values),
        "num_zero_den_positive_count": int(frame["is_num_zero_den_positive"].sum()),
    }
    quantiles = (
        [np.nan] * 5 if len(values) == 0 else np.quantile(values, [0.05, 0.25, 0.5, 0.75, 0.95])
    )
    row.update(
        {
            "mean": float(np.mean(values)) if len(values) else np.nan,
            "p5": quantiles[0],
            "p25": quantiles[1],
            "p50": quantiles[2],
            "p75": quantiles[3],
            "p95": quantiles[4],
        }
    )
    return row


def grouped_summary(ratios_table, group_columns):
    """Summarize FU ratios."""
    rows = []
    for keys, group in ratios_table.groupby(group_columns, sort=False):
        keys = keys if isinstance(keys, tuple) else (keys,)
        group_values = dict(zip(group_columns, keys, strict=True))
        rows.append({**group_values, **summary_row(group, "combined_fu_ratio", COMBINED_FU_RATIO)})

        for fu_ratio, frame in group.groupby("fu_ratio", sort=False):
            row = summary_row(frame, "fu_ratio", fu_ratio)
            rows.append({**group_values, **row})

    return pd.DataFrame(rows)


def world_summary(ratios_table):
    """Build aggregated FU ratios rows and 12 per allocation method ratio rows."""
    rows = []
    for (fu_ratio, label), frame in ratios_table.groupby(["fu_ratio", "ratio_label"], sort=False):
        rows.append(summary_row(frame, "allocation_method_ratio", fu_ratio, label))
    for fu_ratio, frame in ratios_table.groupby("fu_ratio", sort=False):
        row = summary_row(frame, "fu_ratio", fu_ratio)
        rows.append(row)
    rows.append(summary_row(ratios_table, "combined_fu_ratio", COMBINED_FU_RATIO))
    return pd.DataFrame(rows)


# Build the ratio distribution and summary tables from the deterministic aSoCC CSVs.
compiled_asocc = pd.concat(
    [l2_rows(output_root, output_fu) for output_fu, output_root in asocc_roots.items()],
    ignore_index=True,
)
ratio_distribution = build_distribution(compiled_asocc)
world_stats = world_summary(ratio_distribution)
sector_country_stats = grouped_summary(ratio_distribution, ["country", "sector", "year"])

RATIO_CSV_DIR.mkdir(parents=True, exist_ok=True)
ratio_distribution.to_csv(RATIO_CSV_DIR / "allocation_ratio_distribution.csv", index=False)
world_stats.to_csv(RATIO_CSV_DIR / "allocation_ratio_stats_world.csv", index=False)
sector_country_stats.to_csv(
    RATIO_CSV_DIR / "allocation_ratio_stats_by_sector_country.csv",
    index=False,
)

print(f"Distribution CSV: {RATIO_CSV_DIR / 'allocation_ratio_distribution.csv'}")
print(f"World stats CSV: {RATIO_CSV_DIR / 'allocation_ratio_stats_world.csv'}")
print(f"Sector-country stats CSV: {RATIO_CSV_DIR / 'allocation_ratio_stats_by_sector_country.csv'}")
print(f"Distribution rows: {len(ratio_distribution)}")
