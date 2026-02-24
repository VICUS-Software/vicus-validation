#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Validation runner for NANDRAD / EnergyPlus / TRNSYS comparisons.

- Optionally runs EnergyPlus and NANDRAD.
- Reads results: ESO (EnergyPlus), TSVs from NANDRAD, whitespace-delimited TRNSYS table.
- Builds interactive hourly plots (Plotly) and monthly bar charts (Matplotlib).
- Exports hourly/monthly TSV tables and SVG charts.
- Writes where maxima occur (global & per-month) for all series.
- Writes where minima occur (global & per-month) for Air Temperature.
- Writes mean Air Temperature as TSV (global per series + monthly per series).

Key improvements:
- No global variables; explicit data flow.
- Consistent helpers (ESO/TRNSYS/NANDRAD), strict column checks.
- Single hourly datetime index for a configurable year.
- Clear logging with ANSI colors.
"""

from __future__ import annotations

import argparse
import datetime as dt
import locale
import logging
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

import esoreader
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px


# =========================
# Constants & utils
# =========================

HOURS_PER_YEAR = 8759
J_TO_KWH = 1.0 / (3600.0 * 1000.0)
W_TO_KW  = 1.0 / 1000.0

class Ansi:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def setup_logging(quiet: bool = False) -> None:
    """Configure logging format and level."""
    logging.basicConfig(
        level=(logging.INFO if quiet else logging.DEBUG),
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )


def ensure_exists(path: Path, what: str = "file") -> None:
    """Raise if a file/folder does not exist."""
    if not path.exists():
        raise FileNotFoundError(f"{what.capitalize()} not found: {path}")


def build_hourly_index(year: int) -> pd.DatetimeIndex:
    """Construct an hourly DatetimeIndex for a full (non-leap) year."""
    start = dt.datetime(year, 1, 1, 0, 0)
    end = start + dt.timedelta(hours=HOURS_PER_YEAR - 3)
    return pd.date_range(start=start, end=end, freq="h")


# =========================
# I/O
# =========================

def read_tsv(path: Path) -> pd.DataFrame:
    """Load a tab-separated file."""
    ensure_exists(path)
    return pd.read_csv(path, sep="\t")


def read_trnsys_table(path: Path) -> pd.DataFrame:
    """Load TRNSYS results (latin1, whitespace-delimited) and strip string columns."""
    ensure_exists(path)
    df = pd.read_csv(path, encoding="latin1", delim_whitespace=True)
    return df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


def read_reference(path: Path) -> pd.DataFrame:
    """Load reference min/max table and set 'Month' as index."""
    df = read_tsv(path)
    if "Month" not in df.columns:
        raise KeyError(f"Reference must contain 'Month' column: {path}")
    return df.set_index("Month")


@dataclass(frozen=True)
class LoadedData:
    eso: Optional[esoreader.Eso]
    trnsys: Optional[pd.DataFrame]
    air_temp: pd.DataFrame
    cooling: pd.DataFrame
    heating: pd.DataFrame
    window: pd.DataFrame
    ventilation: pd.DataFrame
    radiation: pd.DataFrame
    reference: pd.DataFrame
    direct_shading: Optional[pd.DataFrame] = None
    diffuse_shading: Optional[pd.DataFrame] = None
    direct_sw_radiation: Optional[pd.DataFrame] = None
    diffuse_sw_radiation: Optional[pd.DataFrame] = None


@dataclass(frozen=True)
class AnnualReferences:
    annual: pd.DataFrame       # from annual-references.tsv (Case indexed)
    free_float: pd.DataFrame   # from free-float-references.tsv (Case indexed)


def load_all(nandrad_dir: Path, eso_file: Path, trnsys_file: Path, reference_file: Path) -> LoadedData:
    """Load all required datasets for validation.

    EnergyPlus (ESO) and TRNSYS results are optional — if the files are
    missing the corresponding field in LoadedData will be None and
    process_and_validate() will produce NANDRAD-only outputs.
    """
    logging.info("%sLoading data...%s", Ansi.OKBLUE, Ansi.ENDC)

    eso = None
    if eso_file.exists():
        eso = esoreader.read_from_path(str(eso_file))
    else:
        logging.warning("%sEnergyPlus ESO not found (%s) — continuing without E+ data.%s",
                        Ansi.WARNING, eso_file, Ansi.ENDC)

    trnsys = None
    if trnsys_file.exists():
        trnsys = read_trnsys_table(trnsys_file)
    else:
        logging.warning("%sTRNSYS output not found (%s) — continuing without TRNSYS data.%s",
                        Ansi.WARNING, trnsys_file, Ansi.ENDC)

    air_temp    = read_tsv(nandrad_dir / "results/AirTemperature-Hourly.tsv")
    cooling     = read_tsv(nandrad_dir / "results/IdealCoolingLoad-mean-Hourly.tsv")
    heating     = read_tsv(nandrad_dir / "results/IdealHeatingLoad-mean-Hourly.tsv")
    window      = read_tsv(nandrad_dir / "results/WindowOutputs.tsv")
    ventilation = read_tsv(nandrad_dir / "results/VentilationHeatLoad-mean-Hourly.tsv")
    radiation   = read_tsv(nandrad_dir / "results/RadiationLoadsOutputs.tsv")
    reference   = read_reference(reference_file)

    # Load shading factors (optional - may not exist for all cases)
    direct_shading = None
    diffuse_shading = None
    direct_shading_path = nandrad_dir / "results/DirectShadingFactor-Hourly.tsv"
    diffuse_shading_path = nandrad_dir / "results/DiffuseShadingFactor-Hourly.tsv"
    if direct_shading_path.exists():
        direct_shading = read_tsv(direct_shading_path)
        logging.info("Loaded DirectShadingFactor data")
    if diffuse_shading_path.exists():
        diffuse_shading = read_tsv(diffuse_shading_path)
        logging.info("Loaded DiffuseShadingFactor data")

    # Load imposed radiation (optional - may not exist for all cases)
    direct_sw_radiation = None
    diffuse_sw_radiation = None
    direct_sw_path = nandrad_dir / "results/DirectShortWaveRadiation-mean-Hourly.tsv"
    diffuse_sw_path = nandrad_dir / "results/DiffuseShortWaveRadiation-mean-Hourly.tsv"
    if direct_sw_path.exists():
        direct_sw_radiation = read_tsv(direct_sw_path)
        logging.info("Loaded DirectShortWaveRadiation data")
    if diffuse_sw_path.exists():
        diffuse_sw_radiation = read_tsv(diffuse_sw_path)
        logging.info("Loaded DiffuseShortWaveRadiation data")

    return LoadedData(eso, trnsys, air_temp, cooling, heating, window, ventilation, radiation, reference,
                      direct_shading, diffuse_shading, direct_sw_radiation, diffuse_sw_radiation)


def load_annual_references(ref_dir: Path) -> Optional[AnnualReferences]:
    """Load annual and free-float reference TSV files if they exist."""
    annual_path = ref_dir / "annual-references.tsv"
    ff_path = ref_dir / "free-float-references.tsv"

    if not annual_path.exists():
        logging.warning("Annual reference file not found: %s", annual_path)
        return None

    annual = pd.read_csv(annual_path, sep="\t").set_index("Case")
    annual.index = annual.index.astype(str).str.strip()

    if ff_path.exists():
        ff = pd.read_csv(ff_path, sep="\t").set_index("Case")
        ff.index = ff.index.astype(str).str.strip()
    else:
        ff = pd.DataFrame()
        logging.warning("Free-float reference file not found: %s", ff_path)

    return AnnualReferences(annual=annual, free_float=ff)


# =========================
# Series extraction
# =========================

def col_by_substring(df: pd.DataFrame, needle: str) -> pd.Series:
    """Pick exactly one column by substring; error if none/multiple."""
    hits = [c for c in df.columns if needle in c]
    if not hits:
        raise LookupError(f"No column contains '{needle}'. Available: {list(df.columns)}")
    if len(hits) > 1:
        raise LookupError(f"Multiple columns contain '{needle}': {hits}")
    s = df[hits[0]]
    return pd.to_numeric(s, errors="coerce")


def eso_series(eso: esoreader.Eso, var: str, key: Optional[str], frequency: str = "Hourly") -> pd.Series:
    """Extract a single numeric Series from ESO by variable name and optional key."""
    try:
        df = eso.to_frame(var, frequency=frequency, key=(key if key else ""))
    except Exception as e:
        raise LookupError(f"ESO variable not found: '{var}' (key='{key}', freq='{frequency}') | {e}") from e

    if isinstance(df, pd.Series):
        s = df
    else:
        if df.shape[1] != 1:
            raise LookupError(f"ESO var '{var}' produced {df.shape[1]} columns; specify key.")
        s = df.iloc[:, 0]
    return pd.to_numeric(s, errors="coerce")


def trnsys_series(trnsys_df: pd.DataFrame, col: str) -> pd.Series:
    """Extract TRNSYS column, apply numeric coercion, drop first row, shift by 1 hour."""
    if col not in trnsys_df.columns:
        raise LookupError(f"TRNSYS column '{col}' not found. Available: {list(trnsys_df.columns)}")
    s = pd.to_numeric(trnsys_df[col], errors="coerce")
    s = s.iloc[1:].reset_index(drop=True)  # skip first row as in original
    s = s.shift(1).fillna(0.0)            # align by shifting 1 hour
    return s


# =========================
# Plotting & exports
# =========================

def save_hourly_outputs(df: pd.DataFrame, out_tsv: Path, out_html: Path, title: str, y_label: str) -> None:
    """Save hourly TSV and interactive HTML line plot."""
    df.to_csv(out_tsv, sep="\t", index=True, index_label="Datetime")
    logging.info("Saved hourly TSV: %s", out_tsv)

    fig = px.line(df, x=df.index, y=df.columns, template="plotly_white", title=title)
    fig.update_layout(yaxis_title=y_label, xaxis_title="")
    fig.write_html(out_html)
    logging.info("Saved hourly HTML: %s", out_html)


def save_monthly_bar_with_ref(df_m: pd.DataFrame, title: str, case: str, variant: str, out_svg: Path, is_max_value: bool = False) -> None:
    """Save monthly bar chart with optional min/max overlays."""
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    title = title.replace("W/m²", "Wh/m²")
    if (is_max_value):
        title = title.replace("energie", "last")
        title = title.replace("h]", "]")

    plot_cols = [c for c in df_m.columns if c not in ("min", "max")]
    df_m[plot_cols].plot(kind="bar", ax=ax, width=0.8, legend=True)

    if {"min", "max"}.issubset(df_m.columns):
        xs = np.arange(len(df_m.index))
        ax.plot(xs, df_m["min"].values, linestyle="None", color="black",
                marker="_", markersize=10, mew=2, label="Reference Min")
        ax.plot(xs, df_m["max"].values, linestyle="None", color="black",
                marker="+", markersize=10, mew=2, label="Reference Max")

    ax.set_title(f"{title} | Fall {case}")
    ax.set_xlabel("Monat")
    ax.set_ylabel(title)
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    fig.tight_layout()

    fig.savefig(out_svg, format="svg")
    plt.close(fig)
    logging.info("Saved monthly SVG: %s", out_svg)


# =========================
# Maxima, minima, mean reporting
# =========================

def _save_max_points(
    df_hourly: pd.DataFrame,
    output_dir: Path,
    case: str,
    variant: str,
    base_name: str,
) -> None:
    """Save (a) global maxima with timestamps and (b) per-month maxima with timestamps for each series."""
    # (a) Global maxima with timestamp per series
    rows = []
    for col in df_hourly.columns:
        s = pd.to_numeric(df_hourly[col], errors="coerce")
        idx = s.idxmax()
        val = s.loc[idx] if pd.notna(idx) else np.nan
        rows.append({
            "Series": col,
            "MaxValue": float(val) if pd.notna(val) else np.nan,
            "Timestamp": idx.isoformat() if pd.notna(idx) else ""
        })
    df_global = pd.DataFrame(rows, columns=["Series", "MaxValue", "Timestamp"])
    out_global = output_dir / f"Case{case}_{variant}_{base_name}_hourly_global_max.tsv"
    df_global.to_csv(out_global, sep="\t", index=False)
    logging.info("Saved global max points: %s", out_global)

    # (b) Monthly maxima with timestamp per series
    monthly_rows = []
    for col in df_hourly.columns:
        s = pd.to_numeric(df_hourly[col], errors="coerce")
        for month_end, s_month in s.groupby(pd.Grouper(freq="ME")):
            if s_month.empty:
                continue
            idx = s_month.idxmax()
            val = s_month.loc[idx]
            monthly_rows.append({
                "MonthEnd": month_end.strftime("%Y-%m-%d"),
                "Series": col,
                "Timestamp": idx.isoformat(),
                "MaxValue": float(val)
            })
    df_monthly_pts = pd.DataFrame(monthly_rows, columns=["MonthEnd", "Series", "Timestamp", "MaxValue"])
    out_monthly_pts = output_dir / f"Case{case}_{variant}_{base_name}_monthly_max_points.tsv"
    df_monthly_pts.to_csv(out_monthly_pts, sep="\t", index=False)
    
    logging.info("Saved monthly max points: %s", out_monthly_pts)


def _save_min_points(
    df_hourly: pd.DataFrame,
    output_dir: Path,
    case: str,
    variant: str,
    base_name: str,
) -> None:
    """Save (a) global minima with timestamps and (b) per-month minima with timestamps for each series."""
    # (a) Global minima with timestamp per series
    rows = []
    for col in df_hourly.columns:
        s = pd.to_numeric(df_hourly[col], errors="coerce")
        idx = s.idxmin()
        val = s.loc[idx] if pd.notna(idx) else np.nan
        rows.append({
            "Series": col,
            "MinValue": float(val) if pd.notna(val) else np.nan,
            "Timestamp": idx.isoformat() if pd.notna(idx) else ""
        })
    df_global = pd.DataFrame(rows, columns=["Series", "MinValue", "Timestamp"])
    out_global = output_dir / f"Case{case}_{variant}_{base_name}_hourly_global_min.tsv"
    df_global.to_csv(out_global, sep="\t", index=False)
    logging.info("Saved global min points: %s", out_global)

    # (b) Monthly minima with timestamp per series
    monthly_rows = []
    for col in df_hourly.columns:
        s = pd.to_numeric(df_hourly[col], errors="coerce")
        for month_end, s_month in s.groupby(pd.Grouper(freq="ME")):
            if s_month.empty:
                continue
            idx = s_month.idxmin()
            val = s_month.loc[idx]
            monthly_rows.append({
                "MonthEnd": month_end.strftime("%Y-%m-%d"),
                "Series": col,
                "Timestamp": idx.isoformat(),
                "MinValue": float(val)
            })
    df_monthly_pts = pd.DataFrame(monthly_rows, columns=["MonthEnd", "Series", "Timestamp", "MinValue"])
    out_monthly_pts = output_dir / f"Case{case}_{variant}_{base_name}_monthly_min_points.tsv"
    df_monthly_pts.to_csv(out_monthly_pts, sep="\t", index=False)
    logging.info("Saved monthly min points: %s", out_monthly_pts)


def _save_mean_air_temperature(
    df_hourly: pd.DataFrame,
    output_dir: Path,
    case: str,
    variant: str,
    base_name: str,
) -> None:
    """
    Save mean Air Temperature as TSV:
    - Global mean per series (one row per series).
    - Monthly mean per series (one row per month per series).
    """
    # Global mean per series
    rows = []
    for col in df_hourly.columns:
        s = pd.to_numeric(df_hourly[col], errors="coerce")
        rows.append({
            "Series": col,
            "MeanValue": float(s.mean())
        })
    df_global_mean = pd.DataFrame(rows, columns=["Series", "MeanValue"])
    out_global_mean = output_dir / f"Case{case}_{variant}_{base_name}_hourly_global_mean.tsv"
    df_global_mean.to_csv(out_global_mean, sep="\t", index=False)
    logging.info("Saved global mean air temperature: %s", out_global_mean)

    # Monthly mean per series
    monthly_rows = []
    for col in df_hourly.columns:
        s = pd.to_numeric(df_hourly[col], errors="coerce")
        for month_end, s_month in s.groupby(pd.Grouper(freq="ME")):
            if s_month.empty:
                continue
            monthly_rows.append({
                "MonthEnd": month_end.strftime("%Y-%m-%d"),
                "Series": col,
                "MeanValue": float(s_month.mean())
            })
    df_monthly_mean = pd.DataFrame(monthly_rows, columns=["MonthEnd", "Series", "MeanValue"])
    out_monthly_mean = output_dir / f"Case{case}_{variant}_{base_name}_monthly_mean_points.tsv"
    df_monthly_mean.to_csv(out_monthly_mean, sep="\t", index=False)
    logging.info("Saved monthly mean air temperature: %s", out_monthly_mean)


# =========================
# Reference checking
# =========================

def _check_range(value: float, ref_min: float, ref_max: float) -> str:
    """Return 'PASS' if value is within [ref_min, ref_max], else 'FAIL'."""
    if pd.isna(ref_min) or pd.isna(ref_max):
        return "SKIP"
    if ref_min <= value <= ref_max:
        return "PASS"
    return "FAIL"


def check_annual_references(
    nandrad_annual_heating_kwh: float,
    nandrad_annual_cooling_kwh: float,
    case: str,
    annual_refs: pd.DataFrame,
) -> list[dict]:
    """Compare NANDRAD annual heating/cooling totals against reference bands.

    Annual references are in MWh, NANDRAD values come in kWh -> convert.
    """
    results = []
    nandrad_heating_mwh = nandrad_annual_heating_kwh / 1000.0
    nandrad_cooling_mwh = nandrad_annual_cooling_kwh / 1000.0

    if case in annual_refs.index:
        row = annual_refs.loc[case]
        # Annual heating
        results.append({
            "metric": "Jährliche Heizenergie [MWh]",
            "case": case,
            "nandrad_value": round(nandrad_heating_mwh, 4),
            "ref_min": row.get("heating_min"),
            "ref_max": row.get("heating_max"),
            "status": _check_range(nandrad_heating_mwh,
                                   row.get("heating_min", float("nan")),
                                   row.get("heating_max", float("nan"))),
        })
        # Annual cooling
        results.append({
            "metric": "Jährliche Kühlenergie [MWh]",
            "case": case,
            "nandrad_value": round(nandrad_cooling_mwh, 4),
            "ref_min": row.get("cooling_min"),
            "ref_max": row.get("cooling_max"),
            "status": _check_range(nandrad_cooling_mwh,
                                   row.get("cooling_min", float("nan")),
                                   row.get("cooling_max", float("nan"))),
        })
    else:
        logging.info("No annual references for Case %s", case)

    return results


def check_peak_references(
    nandrad_peak_heating_kw: float,
    nandrad_peak_cooling_kw: float,
    case: str,
    annual_refs: pd.DataFrame,
) -> list[dict]:
    """Compare NANDRAD peak heating/cooling loads against reference bands (kW)."""
    results = []
    if case in annual_refs.index:
        row = annual_refs.loc[case]
        results.append({
            "metric": "Spitzenheizlast [kW]",
            "case": case,
            "nandrad_value": round(nandrad_peak_heating_kw, 4),
            "ref_min": row.get("peak_heating_min"),
            "ref_max": row.get("peak_heating_max"),
            "status": _check_range(nandrad_peak_heating_kw,
                                   row.get("peak_heating_min", float("nan")),
                                   row.get("peak_heating_max", float("nan"))),
        })
        results.append({
            "metric": "Spitzenkühllast [kW]",
            "case": case,
            "nandrad_value": round(nandrad_peak_cooling_kw, 4),
            "ref_min": row.get("peak_cooling_min"),
            "ref_max": row.get("peak_cooling_max"),
            "status": _check_range(nandrad_peak_cooling_kw,
                                   row.get("peak_cooling_min", float("nan")),
                                   row.get("peak_cooling_max", float("nan"))),
        })
    return results


def check_free_float_references(
    nandrad_temp_max: float,
    nandrad_temp_min: float,
    nandrad_temp_avg: float,
    case: str,
    ff_refs: pd.DataFrame,
) -> list[dict]:
    """Compare NANDRAD free-float temperatures against reference bands."""
    results = []
    if ff_refs.empty or case not in ff_refs.index:
        logging.info("No free-float references for Case %s", case)
        return results

    row = ff_refs.loc[case]
    results.append({
        "metric": "Max. Lufttemperatur [°C]",
        "case": case,
        "nandrad_value": round(nandrad_temp_max, 2),
        "ref_min": row.get("temp_max_min"),
        "ref_max": row.get("temp_max_max"),
        "status": _check_range(nandrad_temp_max,
                               row.get("temp_max_min", float("nan")),
                               row.get("temp_max_max", float("nan"))),
    })
    results.append({
        "metric": "Min. Lufttemperatur [°C]",
        "case": case,
        "nandrad_value": round(nandrad_temp_min, 2),
        "ref_min": row.get("temp_min_min"),
        "ref_max": row.get("temp_min_max"),
        "status": _check_range(nandrad_temp_min,
                               row.get("temp_min_min", float("nan")),
                               row.get("temp_min_max", float("nan"))),
    })
    results.append({
        "metric": "Mittl. Lufttemperatur [°C]",
        "case": case,
        "nandrad_value": round(nandrad_temp_avg, 2),
        "ref_min": row.get("temp_avg_min"),
        "ref_max": row.get("temp_avg_max"),
        "status": _check_range(nandrad_temp_avg,
                               row.get("temp_avg_min", float("nan")),
                               row.get("temp_avg_max", float("nan"))),
    })
    return results


def check_monthly_references(
    df_hourly: pd.DataFrame,
    case: str,
    monthly_refs: pd.DataFrame,
    ref_suffix: str,
    metric_label: str,
) -> list[dict]:
    """Compare NANDRAD monthly sums against monthly reference bands."""
    results = []
    min_col = f"Case{case}_{ref_suffix}_min"
    max_col = f"Case{case}_{ref_suffix}_max"

    if min_col not in monthly_refs.columns or max_col not in monthly_refs.columns:
        return results

    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df_m = df_hourly.resample("ME").sum()

    for i, (_, row_m) in enumerate(df_m.iterrows()):
        if i >= 12:
            break
        nandrad_val = row_m.get("NANDRAD", 0.0)
        ref_min_val = monthly_refs.loc[monthly_refs.index == month_labels[i], min_col]
        ref_max_val = monthly_refs.loc[monthly_refs.index == month_labels[i], max_col]
        if ref_min_val.empty or ref_max_val.empty:
            continue
        r_min = float(ref_min_val.iloc[0])
        r_max = float(ref_max_val.iloc[0])
        results.append({
            "metric": f"{metric_label} {month_labels[i]} [kWh]",
            "case": case,
            "nandrad_value": round(float(nandrad_val), 2),
            "ref_min": r_min,
            "ref_max": r_max,
            "status": _check_range(float(nandrad_val), r_min, r_max),
        })
    return results


def generate_validation_report(
    results: list[dict],
    output_dir: Path,
    case: str,
    variant: str,
) -> None:
    """Write validation summary as TSV and styled HTML table."""
    if not results:
        return

    df = pd.DataFrame(results)
    cols = ["metric", "nandrad_value", "ref_min", "ref_max", "status"]
    df = df[cols].rename(columns={
        "metric": "Metrik",
        "nandrad_value": "NANDRAD",
        "ref_min": "Ref Min",
        "ref_max": "Ref Max",
        "status": "Status",
    })

    # TSV
    tsv_path = output_dir / f"Case{case}_{variant}_validation_report.tsv"
    df.to_csv(tsv_path, sep="\t", index=False)
    logging.info("Saved validation report TSV: %s", tsv_path)

    # HTML
    html_path = output_dir / f"Case{case}_{variant}_validation_report.html"

    # Count pass/fail
    n_pass = (df["Status"] == "PASS").sum()
    n_fail = (df["Status"] == "FAIL").sum()
    n_skip = (df["Status"] == "SKIP").sum()
    n_total = len(df)

    def _row_color(status: str) -> str:
        if status == "PASS":
            return "background-color: #d4edda;"
        elif status == "FAIL":
            return "background-color: #f8d7da;"
        return "background-color: #e2e3e5;"

    html_rows = []
    for _, row in df.iterrows():
        style = _row_color(row["Status"])
        cells = "".join(f'<td style="{style}">{v}</td>' for v in row)
        html_rows.append(f"<tr>{cells}</tr>")

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>Validation Report - Case {case} {variant}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 20px; }}
h1 {{ color: #333; }}
.summary {{ margin: 10px 0; font-size: 1.1em; }}
.pass {{ color: #155724; font-weight: bold; }}
.fail {{ color: #721c24; font-weight: bold; }}
.skip {{ color: #383d41; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 15px; }}
th {{ background-color: #343a40; color: white; padding: 10px; text-align: left; }}
td {{ padding: 8px; border-bottom: 1px solid #dee2e6; }}
</style>
</head>
<body>
<h1>ASHRAE 140 Validation Report &mdash; Case {case} ({variant})</h1>
<div class="summary">
  <span class="pass">PASS: {n_pass}</span> &bull;
  <span class="fail">FAIL: {n_fail}</span> &bull;
  <span class="skip">SKIP: {n_skip}</span> &bull;
  Total: {n_total}
</div>
<table>
<thead><tr>{"".join(f"<th>{c}</th>" for c in df.columns)}</tr></thead>
<tbody>
{"".join(html_rows)}
</tbody>
</table>
</body>
</html>"""

    html_path.write_text(html, encoding="utf-8")
    logging.info("Saved validation report HTML: %s", html_path)

    # Summary log
    if n_fail > 0:
        logging.warning("%s%sValidation: %d/%d FAIL%s", Ansi.FAIL, Ansi.BOLD, n_fail, n_total, Ansi.ENDC)
    else:
        logging.info("%s%sValidation: %d/%d PASS%s", Ansi.OKGREEN, Ansi.BOLD, n_pass, n_total, Ansi.ENDC)


# =========================
# Core validation step
# =========================

def process_and_validate(
    *,
    title: str,
    y_axis_label: str,
    output_dir: Path,
    case: str,
    variant: str,
    year: int,
    data: LoadedData,
    nandrad_df: pd.DataFrame,
    nandrad_col_substr: str,
    ep_var: str,
    ep_key: Optional[str],
    trnsys_col: str,
    nandrad_conv: float = 1.0,
    ep_conv: float = 1.0,
    trnsys_conv: float = 1.0,
    ep_subtract_var: Optional[str] = None,
    ep_subtract_key: Optional[str] = None,
    ep_subtract_conv: float = 1.0,
    create_monthly_summary: bool = False,
    unit: str = "",
    ref_suffix: str = "",
    results_collector: Optional[list] = None,
) -> Optional[pd.DataFrame]:
    """Produce hourly comparison (NANDRAD vs EnergyPlus vs TRNSYS) and optional monthly summaries.

    Returns the hourly DataFrame if successful, None otherwise.
    If results_collector is provided, appends monthly pass/fail dicts to it.
    """
    logging.info("%s--- Validating: %s %s", Ansi.OKCYAN, title, Ansi.ENDC)
    try:
        # --- Extract series from NANDRAD (always required) ---
        s_nand = col_by_substring(nandrad_df, nandrad_col_substr) * nandrad_conv

        # --- Extract EnergyPlus series (optional) ---
        s_ep = None
        if data.eso is not None:
            try:
                s_ep = eso_series(data.eso, var=ep_var, key=ep_key, frequency="Hourly") * ep_conv
                if ep_subtract_var:
                    s_sub = eso_series(data.eso, var=ep_subtract_var, key=ep_subtract_key, frequency="Hourly")
                    s_sub *= ep_subtract_conv
                    s_ep = s_ep - s_sub
            except LookupError as e:
                logging.warning("EnergyPlus data unavailable for '%s': %s", title, e)

        # --- Extract TRNSYS series (optional) ---
        s_trn = None
        if data.trnsys is not None:
            try:
                s_trn = trnsys_series(data.trnsys, trnsys_col) * trnsys_conv
            except LookupError as e:
                logging.warning("TRNSYS data unavailable for '%s': %s", title, e)

        # --- Assemble hourly DataFrame on a shared datetime index ---
        idx = build_hourly_index(year)
        df_hourly = pd.DataFrame(index=idx)
        df_hourly["NANDRAD"]    = s_nand.values[1:HOURS_PER_YEAR-1]
        if s_ep is not None:
            df_hourly["EnergyPlus"] = s_ep.values[:HOURS_PER_YEAR-2]
        if s_trn is not None:
            df_hourly["TRNSYS"]     = s_trn.values[2:HOURS_PER_YEAR]
        df_hourly = df_hourly.fillna(0.0)

        # --- Save hourly outputs ---
        base = title.replace(" ", "_")
        title = title + f" [{unit}]"

        out_tsv  = output_dir / f"Case{case}_{variant}_{base}_hourly.tsv"
        out_html = output_dir / f"Case{case}_{variant}_{base}_hourly.html"
        save_hourly_outputs(df_hourly, out_tsv, out_html, title, y_axis_label)

        # --- Always write max points (global + monthly) ---
        _save_max_points(
            df_hourly=df_hourly,
            output_dir=output_dir,
            case=case,
            variant=variant,
            base_name=base,
        )

        # --- For Air Temperature only: also write min + mean points ---
        if title == "Lufttemperatur [C]":
            _save_min_points(
                df_hourly=df_hourly,
                output_dir=output_dir,
                case=case,
                variant=variant,
                base_name=base,
            )
            _save_mean_air_temperature(
                df_hourly=df_hourly,
                output_dir=output_dir,
                case=case,
                variant=variant,
                base_name=base,
            )

        # --- Monthly summaries (sum) and optional reference bands ---
        if create_monthly_summary:
            # Try to get English month labels (Linux/Windows)
            try:
                locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
            except locale.Error:
                try:
                    locale.setlocale(locale.LC_TIME, "English_United States.1252")
                except locale.Error:
                    pass

            df_y = df_hourly.resample("YE").sum()

            df_m = df_hourly.resample("ME").sum()
            df_m.index = df_m.index.strftime("%b")

            try:
                if ref_suffix:
                    min_col = f"Case{case}_{ref_suffix}_min"
                    max_col = f"Case{case}_{ref_suffix}_max"
                    if min_col not in data.reference.columns or max_col not in data.reference.columns:
                        raise KeyError(f"Missing reference columns '{min_col}'/'{max_col}' in reference table.")
                    df_m["min"] = data.reference[min_col].values
                    df_m["max"] = data.reference[max_col].values
            except Exception as e:
                logging.warning("Could not find any references for test-case. Skipping reference application.")

            out_y_sum = output_dir / f"Case{case}_{variant}_{base}_yearly_sum.tsv"
            df_y.to_csv(out_y_sum, sep="\t")
            logging.info("Saved yearly TSV (sum): %s", out_y_sum)

            out_m_sum = output_dir / f"Case{case}_{variant}_{base}_monthly_sum.tsv"
            df_m.to_csv(out_m_sum, sep="\t")
            logging.info("Saved monthly TSV (sum): %s", out_m_sum)

            out_svg = output_dir / f"Case{case}_{variant}_{base}_monthly_mean.svg"
            save_monthly_bar_with_ref(df_m, title, case, variant, out_svg)

            # Additional monthly exports matching original behavior
            df_m_integral = df_hourly.resample("ME").sum()
            df_m_integral.index = df_m_integral.index.strftime("%Y-%m-%d %H:%M")
            (output_dir / f"Case{case}_{variant}_{base}_monthly_integral.tsv").write_text(
                df_m_integral.to_csv(sep="\t")
            )

            df_m_max = df_hourly.resample("ME").max()
            df_m_max.index = df_m_max.index.strftime("%Y-%m-%d %H:%M")
            (output_dir / f"Case{case}_{variant}_{base}_monthly_max.tsv").write_text(
                df_m_max.to_csv(sep="\t")
            )

            df_m_max = df_hourly.resample("ME").max()
            df_m_max.index = df_m_max.index.strftime("%b")
            save_monthly_bar_with_ref(df_m_max, title, case, variant,
                              output_dir / f"Case{case}_{variant}_{base}_monthly_max.svg", True)

            # --- Monthly reference checks ---
            if results_collector is not None and ref_suffix:
                monthly_results = check_monthly_references(
                    df_hourly, case, data.reference, ref_suffix,
                    metric_label=base,
                )
                results_collector.extend(monthly_results)

        return df_hourly

    except (LookupError, KeyError, FileNotFoundError) as e:
        logging.warning("%sSkipping '%s'. Reason: %s%s", Ansi.WARNING, title, e, Ansi.ENDC)
    except Exception as e:
        logging.error("%sUnexpected error in '%s': %s%s", Ansi.FAIL, title, e, Ansi.ENDC, exc_info=True)
    return None


# =========================
# Simulation runners
# =========================

def run_energyplus(exec_path: Path, idf_file: Path, weather_file: Path, workdir: Path) -> None:
    """Run EnergyPlus with provided IDF and EPW."""
    ensure_exists(exec_path, "executable")
    ensure_exists(idf_file)
    ensure_exists(weather_file)
    ensure_exists(workdir, "folder")

    cmd = [str(exec_path), "-w", str(weather_file), str(idf_file)]
    logging.info("%sEnergyPlus:%s %s", Ansi.BOLD, Ansi.ENDC, " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=workdir)


def run_nandrad(exec_path: Path, nandrad_file: Path, workdir: Path) -> None:
    """Run NANDRAD solver with input file."""
    ensure_exists(exec_path, "executable")
    ensure_exists(nandrad_file)
    ensure_exists(workdir, "folder")

    cmd = [str(exec_path), "-x", str(nandrad_file)]
    logging.info("%sNANDRAD:%s %s", Ansi.BOLD, Ansi.ENDC, " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=workdir)


# =========================
# CLI
# =========================

def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run and validate NANDRAD / EnergyPlus / TRNSYS outputs.")
    parser.add_argument("-c", "--case", default="600", help="Test case (e.g., 600, 630)")
    parser.add_argument("-v", "--variant", default="v2", help="Variant label (e.g., v1)")
    parser.add_argument("-y", "--year", type=int, default=2021, help="Calendar year for hourly index")
    parser.add_argument("-w", "--windows",
        default="ZONE SUBSURFACE 1",
        help="Comma-separated EP window keys (e.g., 'ZONE SUBSURFACE 1,ZONE SUBSURFACE 2')"
    )
    parser.add_argument("--data-dir", type=Path, default=Path.cwd() / "data", help="Root data directory")
    parser.add_argument("--out-dir", type=Path, default=Path.cwd() / "validation_results", help="Output root directory")
    parser.add_argument("--ep-exec", type=Path,
        default=(Path("C:/EnergyPlusV9-0-1/energyplus.exe") if os.name == "nt"
                 else Path("/home/hirth/Applikationen/EnergyPlus-9-0-1/energyplus"))
    )
    parser.add_argument("--nandrad-exec", type=Path,
        default=(Path("C:/Program Files/VICUS-Software/VICUS/NandradSolver.exe") if os.name == "nt"
                 else Path.cwd() / "bin" / "NandradSolver")
    )
    parser.add_argument("--epw", type=Path, default=Path.cwd() / "data" / "climate" / "725650TYCST.epw",
                        help="Path to the EPW file")
    parser.add_argument("--skip-run", action="store_true", help="Skip running simulations; only read/validate")
    parser.add_argument("-q", "--quiet", action="store_true", default=True, help="Reduce log verbosity")
    return parser.parse_args(argv)


# =========================
# Main
# =========================

def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    setup_logging(quiet=args.quiet)

    case = str(args.case)
    variant = str(args.variant)
    year = int(args.year)
    window_keys = [w.strip() for w in args.windows.split(",") if w.strip()]

    # Resolve folders and files
    data_dir = args.data_dir
    out_dir = args.out_dir / f"Case{case}_{variant}"
    out_dir.mkdir(parents=True, exist_ok=True)

    nandrad_dir   = data_dir / "nandrad" / f"Case{case}_{variant}"
    nandrad_file  = data_dir / "nandrad" / f"Case{case}_{variant}.nandrad"
    energy_dir    = data_dir / "energyplus"
    idf_file      = energy_dir / f"Case{case}_{variant}.idf"
    eso_file      = energy_dir / "eplusout.eso"
    trnsys_file   = data_dir / "trnsys" / f"CASE{case}.out"
    reference_tbl = data_dir / "reference" / "monthly-references.tsv"
    epw_file      = args.epw

    try:
        if not args.skip_run:
            logging.info("%s--- Running simulations ---%s", Ansi.BOLD, Ansi.ENDC)
            if idf_file.exists() and args.ep_exec.exists():
                run_energyplus(args.ep_exec, idf_file, epw_file, workdir=energy_dir)
            else:
                logging.warning("%sSkipping EnergyPlus (IDF or executable not found).%s",
                                Ansi.WARNING, Ansi.ENDC)
            if nandrad_file.exists() and args.nandrad_exec.exists():
                run_nandrad(args.nandrad_exec, nandrad_file, workdir=nandrad_dir.parent)
            else:
                logging.warning("%sSkipping NANDRAD (file or executable not found).%s",
                                Ansi.WARNING, Ansi.ENDC)
            logging.info("%sSimulations finished.%s", Ansi.OKGREEN, Ansi.ENDC)
        else:
            logging.info("Skipping simulation runs (--skip-run).")

        # Load outputs
        data = load_all(nandrad_dir, eso_file, trnsys_file, reference_tbl)

        # Load annual/peak/free-float references
        annual_refs = load_annual_references(data_dir / "reference")

        # Collector for pass/fail results
        validation_results: list[dict] = []

        # For multi-zone cases (e.g. 960 sunspace), prefix NANDRAD column
        # searches to select only the conditioned zone.
        # Column pattern: "Case 960.Back Zone(ID=3).IdealHeatingLoad-average [W]"
        nz = "Back Zone(ID=3)." if case == "960" else ""

        logging.info("%s--- Generating validation for Case %s %s ---%s",
                     Ansi.BOLD, case, variant, Ansi.ENDC)

        # --- Air Temperature (hourly; outputs min, max, mean TSVs) ---
        df_air_temp = process_and_validate(
            title="Lufttemperatur",
            y_axis_label="Temperatur [°C]",
            output_dir=out_dir,
            case=case,
            variant=variant,
            year=year,
            data=data,
            nandrad_df=data.air_temp,
            nandrad_col_substr=f"{nz}AirTemperature",
            ep_var="Zone Mean Air Temperature",
            ep_key="ZONE ONE",
            trnsys_col="Tzone",
            unit="C",
            results_collector=validation_results,
        )

        # --- Zone Windows Total Transmitted (monthly with ref) ---
        process_and_validate(
            title="Transmittierte kurzwellige Strahlung Fenster",
            y_axis_label="Strahlung [W/m²]",
            output_dir=out_dir,
            case=case,
            variant=variant,
            year=year,
            data=data,
            nandrad_df=data.window,
            nandrad_col_substr="WindowSolarRadiationFluxSum",
            ep_var="Zone Windows Total Transmitted Solar Radiation Rate",
            ep_key="ZONE ONE",
            trnsys_col="QTransmitted",
            nandrad_conv=(1.0 / 12.0),
            ep_conv=(1.0 / 12.0),
            trnsys_conv=1000.0,
            create_monthly_summary=True,
            unit="W/m²",
            ref_suffix="",
        )

        # --- Absorbed window radiation (kept close to original intent) ---
        process_and_validate(
            title="Absorbierte kurzwellige Strahlung Raumluft",
            y_axis_label="Wärmelast [W/m²]",
            output_dir=out_dir,
            case=case,
            variant=variant,
            year=year,
            data=data,
            nandrad_df=data.window,
            nandrad_col_substr="WindowSolarRadiationFluxSum",
            ep_var="Zone Windows Total Heat Loss Energy",
            ep_key="ZONE ONE",
            trnsys_col="QTransmitted",
            ep_conv=(1.0 / 3600.0),  # J -> W
            unit="W/m²",
        )

        # --- Per-window heat conduction (hourly) ---
        for win_key in window_keys:
            process_and_validate(
                title=f"Wärmeleitung Fenster ({win_key})",
                y_axis_label="Wärmestrom [W/m²]",
                output_dir=out_dir,
                case=case,
                variant=variant,
                year=year,
                data=data,
                nandrad_df=data.window,
                nandrad_col_substr=f"{nz}WindowHeatConductionLoad",
                ep_var="Surface Window Net Heat Transfer Rate",
                ep_key=win_key.upper(),
                trnsys_col="QTransmitted",  # placeholder as in original
                trnsys_conv=0.0,
                ep_subtract_var="Zone Windows Total Transmitted Solar Radiation Rate",
                ep_subtract_key="ZONE ONE",
                ep_subtract_conv=(1.0 / 12.0),
                nandrad_conv=(1.0 / 12.0),
                ep_conv=(1.0 / 6.0),
                unit="W/m²",
            )

        # --- Heating Load (monthly with ref) ---
        df_heating = process_and_validate(
            title="Heizenergie",
            y_axis_label="Energie [kWh]",
            output_dir=out_dir,
            case=case,
            variant=variant,
            year=year,
            data=data,
            nandrad_df=data.heating,
            nandrad_col_substr=f"{nz}IdealHeatingLoad" if nz else "Heating",
            ep_var="Zone Air System Sensible Heating Energy",
            ep_key=None,
            trnsys_col="Qheat",
            ep_conv=J_TO_KWH,
            nandrad_conv=W_TO_KW,
            create_monthly_summary=True,
            unit="kWh",
            ref_suffix="heating",
            results_collector=validation_results,
        )

        # --- Cooling Load (monthly with ref) ---
        df_cooling = process_and_validate(
            title="Kühlenergie",
            y_axis_label="Energie [kWh]",
            output_dir=out_dir,
            case=case,
            variant=variant,
            year=year,
            data=data,
            nandrad_df=data.cooling,
            nandrad_col_substr=f"{nz}IdealCoolingLoad" if nz else "Cooling",
            ep_var="Zone Air System Sensible Cooling Energy",
            ep_key="ZONE ONE",
            trnsys_col="Qcool",
            ep_conv=J_TO_KWH,
            nandrad_conv=W_TO_KW,
            create_monthly_summary=True,
            unit="kWh",
            ref_suffix="cooling",
            results_collector=validation_results,
        )

        # --- Short-wave radiation onto exterior surfaces ---
        process_and_validate(
            title="Kurzwellige Strahlungslasten Horizontal",
            y_axis_label="Strahlung [W/m²]",
            output_dir=out_dir,
            case=case,
            variant=variant,
            year=year,
            data=data,
            nandrad_df=data.radiation,
            nandrad_col_substr="GlobalSWRadOnPlane(id=2000000)",
            ep_var="Surface Outside Face Incident Solar Radiation Rate per Area",
            ep_key="ZONE SURFACE ROOF",
            trnsys_col="SolarH",
            trnsys_conv=1000., # TRNSYS' output unit is not kJ, it is kW/m²!!!
            ep_conv=1.,
            nandrad_conv=1.,
            create_monthly_summary=True,
            unit="W/m²",
            ref_suffix="",
        )
        
        process_and_validate(
            title="Kurzwellige direkte Strahlungslasten Horizontal",
            y_axis_label="Strahlung [W/m²]",
            output_dir=out_dir,
            case=case,
            variant=variant,
            year=year,
            data=data,
            nandrad_df=data.radiation,
            nandrad_col_substr="DirectSWRadOnPlane(id=2000000)",
            ep_var="Surface Outside Face Incident Beam Solar Radiation Rate per Area",
            ep_key="ZONE SURFACE ROOF",
            trnsys_col="SolarH",
            trnsys_conv=0., # TRNSYS' output unit is not kJ, it is kW/m²!!!
            ep_conv=1.,
            nandrad_conv=1.,
            create_monthly_summary=True,
            unit="W/m²",
            ref_suffix="",
        )
                
        process_and_validate(
            title="Kurzwellige diffuse Strahlungslasten Horizontal",
            y_axis_label="Strahlung [W/m²]",
            output_dir=out_dir,
            case=case,
            variant=variant,
            year=year,
            data=data,
            nandrad_df=data.radiation,
            nandrad_col_substr="DiffuseSWRadOnPlane(id=2000000)",
            ep_var="Surface Outside Face Incident Solar Radiation Rate per Area",
            ep_key="ZONE SURFACE ROOF",
            ep_subtract_key="ZONE SURFACE ROOF",
            ep_subtract_var="Surface Outside Face Incident Beam Solar Radiation Rate per Area",
            ep_subtract_conv=1.,
            trnsys_col="SolarH",
            trnsys_conv=0., # TRNSYS' output unit is not kJ, it is kW/m²!!!
            ep_conv=1.,
            nandrad_conv=1.,
            create_monthly_summary=True,
            unit="W/m²",
            ref_suffix="",
        )
        
        process_and_validate(
            title="Kurzwellige Strahlungslasten Nord",
            y_axis_label="Strahlung [W/m²]",
            output_dir=out_dir,
            case=case,
            variant=variant,
            year=year,
            data=data,
            nandrad_df=data.radiation,
            nandrad_col_substr="GlobalSWRadOnPlane(id=2000001)",
            ep_var="Surface Outside Face Incident Solar Radiation Rate per Area",
            ep_key="ZONE SURFACE NORTH",
            trnsys_col="SolarN",
            trnsys_conv=1000., # TRNSYS' output unit is not kJ, it is kW/m²!!!
            ep_conv=1.,
            nandrad_conv=1.,
            create_monthly_summary=True,
            unit="W/m²",
            ref_suffix="",
        )
                
        process_and_validate(
            title="Kurzwellige Strahlungslasten Ost",
            y_axis_label="Strahlung [W/m²]",
            output_dir=out_dir,
            case=case,
            variant=variant,
            year=year,
            data=data,
            nandrad_df=data.radiation,
            nandrad_col_substr="2000002",
            ep_var="Surface Outside Face Incident Solar Radiation Rate per Area",
            ep_key="ZONE SURFACE EAST",
            trnsys_col="SolarE",
            trnsys_conv=1000., # TRNSYS' output unit is not kJ, it is kW/m²!!!
            ep_conv=1.,
            nandrad_conv=1.,
            create_monthly_summary=True,
            unit="W/m²",
            ref_suffix="",
        )
        
        process_and_validate(
            title="Kurzwellige Strahlungslasten Süd",
            y_axis_label="Strahlung [W/m²]",
            output_dir=out_dir,
            case=case,
            variant=variant,
            year=year,
            data=data,
            nandrad_df=data.radiation,
            nandrad_col_substr="2000003",
            ep_var="Surface Outside Face Incident Solar Radiation Rate per Area",
            ep_key="ZONE SURFACE SOUTH",
            trnsys_col="SolarS",
            trnsys_conv=1000., # TRNSYS' output unit is not kJ, it is kW/m²!!!
            ep_conv=1.,
            nandrad_conv=1.,
            create_monthly_summary=True,
            unit="W/m²",
            ref_suffix="",
        )
                
        process_and_validate(
            title="Kurzwellige Strahlungslasten West",
            y_axis_label="Strahlung [W/m²]",
            output_dir=out_dir,
            case=case,
            variant=variant,
            year=year,
            data=data,
            nandrad_df=data.radiation,
            nandrad_col_substr="2000004",
            ep_var="Surface Outside Face Incident Solar Radiation Rate per Area",
            ep_key="ZONE SURFACE WEST",
            trnsys_col="SolarW",
            trnsys_conv=1000., # TRNSYS' output unit is not kJ, it is kW/m²!!!
            ep_conv=1.,
            nandrad_conv=1.,
            create_monthly_summary=True,
            unit="W/m²",
            ref_suffix="",
        )
        
        process_and_validate(
            title="Kurzwellige direkte Strahlungslasten Nord",
            y_axis_label="Strahlung [W/m²]",
            output_dir=out_dir,
            case=case,
            variant=variant,
            year=year,
            data=data,
            nandrad_df=data.radiation,
            nandrad_col_substr="DirectSWRadOnPlane(id=2000001)",
            ep_var="Surface Outside Face Incident Beam Solar Radiation Rate per Area",
            ep_key="ZONE SURFACE NORTH",
            trnsys_col="SolarN",
            trnsys_conv=0., # we don't want to see trnsys results
            ep_conv=1.,
            nandrad_conv=1.,
            create_monthly_summary=True,
            unit="W/m²",
            ref_suffix="",
        )
        
        process_and_validate(
            title="Kurzwellige diffuse Strahlungslasten Nord",
            y_axis_label="Strahlung [W/m²]",
            output_dir=out_dir,
            case=case,
            variant=variant,
            year=year,
            data=data,
            nandrad_df=data.radiation,
            nandrad_col_substr="DiffuseSWRadOnPlane(id=2000001)",
            ep_var="Surface Outside Face Incident Solar Radiation Rate per Area",
            ep_key="ZONE SURFACE NORTH",
            ep_subtract_key="ZONE SURFACE NORTH",
            ep_subtract_var="Surface Outside Face Incident Beam Solar Radiation Rate per Area",
            ep_subtract_conv=1.,
            trnsys_col="SolarN",
            trnsys_conv=0., # we have no trnsys results
            ep_conv=1.,
            nandrad_conv=1.,
            create_monthly_summary=True,
            unit="W/m²",
            ref_suffix="",
        )

        # --- Direct Shading Factor comparisons ---
        if data.direct_shading is not None:
            # Window left (ZONE SUBSURFACE 1)
            process_and_validate(
                title="Direkter Verschattungsfaktor Fenster links",
                y_axis_label="Shading Factor [-]",
                output_dir=out_dir,
                case=case,
                variant=variant,
                year=year,
                data=data,
                nandrad_df=data.direct_shading,
                nandrad_col_substr="Window left",
                ep_var="Surface Outside Face Sunlit Fraction",
                ep_key="ZONE SUBSURFACE 1",
                trnsys_col="Tzone",  # placeholder
                trnsys_conv=0.,
                ep_conv=1.,
                nandrad_conv=1.,
                create_monthly_summary=True,
                unit="-",
                ref_suffix="",
            )
            # Window right (ZONE SUBSURFACE 2)
            process_and_validate(
                title="Direkter Verschattungsfaktor Fenster rechts",
                y_axis_label="Shading Factor [-]",
                output_dir=out_dir,
                case=case,
                variant=variant,
                year=year,
                data=data,
                nandrad_df=data.direct_shading,
                nandrad_col_substr="Window right",
                ep_var="Surface Outside Face Sunlit Fraction",
                ep_key="ZONE SUBSURFACE 2",
                trnsys_col="Tzone",  # placeholder
                trnsys_conv=0.,
                ep_conv=1.,
                nandrad_conv=1.,
                create_monthly_summary=True,
                unit="-",
                ref_suffix="",
            )
            # Wall South
            process_and_validate(
                title="Direkter Verschattungsfaktor Wand Süd",
                y_axis_label="Shading Factor [-]",
                output_dir=out_dir,
                case=case,
                variant=variant,
                year=year,
                data=data,
                nandrad_df=data.direct_shading,
                nandrad_col_substr="Wall South",
                ep_var="Surface Outside Face Sunlit Fraction",
                ep_key="ZONE SURFACE SOUTH",
                trnsys_col="Tzone",  # placeholder
                trnsys_conv=0.,
                ep_conv=1.,
                nandrad_conv=1.,
                create_monthly_summary=True,
                unit="-",
                ref_suffix="",
            )

        # --- Diffuse Shading Factor ---
        # EnergyPlus has Debug Surface Solar Shading Model DifShdgRatioIsoSky
        if data.diffuse_shading is not None:
            # Window left
            process_and_validate(
                title="Diffuser Verschattungsfaktor Fenster links",
                y_axis_label="Shading Factor [-]",
                output_dir=out_dir,
                case=case,
                variant=variant,
                year=year,
                data=data,
                nandrad_df=data.diffuse_shading,
                nandrad_col_substr="Window left",
                ep_var="Debug Surface Solar Shading Model DifShdgRatioIsoSky",
                ep_key="ZONE SUBSURFACE 1",
                trnsys_col="Tzone",  # placeholder
                trnsys_conv=0.,
                ep_conv=1.,
                nandrad_conv=1.,
                create_monthly_summary=True,
                unit="-",
                ref_suffix="",
            )
            # Window right
            process_and_validate(
                title="Diffuser Verschattungsfaktor Fenster rechts",
                y_axis_label="Shading Factor [-]",
                output_dir=out_dir,
                case=case,
                variant=variant,
                year=year,
                data=data,
                nandrad_df=data.diffuse_shading,
                nandrad_col_substr="Window right",
                ep_var="Debug Surface Solar Shading Model DifShdgRatioIsoSky",
                ep_key="ZONE SUBSURFACE 2",
                trnsys_col="Tzone",
                trnsys_conv=0.,
                ep_conv=1.,
                nandrad_conv=1.,
                create_monthly_summary=True,
                unit="-",
                ref_suffix="",
            )
            # Wall South
            process_and_validate(
                title="Diffuser Verschattungsfaktor Wand Süd",
                y_axis_label="Shading Factor [-]",
                output_dir=out_dir,
                case=case,
                variant=variant,
                year=year,
                data=data,
                nandrad_df=data.diffuse_shading,
                nandrad_col_substr="Wall South",
                ep_var="Debug Surface Solar Shading Model DifShdgRatioIsoSky",
                ep_key="ZONE SURFACE SOUTH",
                trnsys_col="Tzone",
                trnsys_conv=0.,
                ep_conv=1.,
                nandrad_conv=1.,
                create_monthly_summary=True,
                unit="-",
                ref_suffix="",
            )
            logging.info("%sDiffuse shading factors: Window=%.3f, Wall South=%.3f%s",
                        Ansi.OKCYAN,
                        data.diffuse_shading.iloc[0, 1] if len(data.diffuse_shading.columns) > 1 else 0,
                        data.diffuse_shading.iloc[0, 3] if len(data.diffuse_shading.columns) > 3 else 0,
                        Ansi.ENDC)

        # --- Total Short Wave Radiation (imposed) comparisons ---
        # EnergyPlus only provides total incident solar for windows, not split into beam/diffuse
        # So we compare NANDRAD's total (Direct + Diffuse) with EP's total incident
        if data.direct_sw_radiation is not None and data.diffuse_sw_radiation is not None:
            # Create combined total radiation dataframe
            total_sw_radiation = data.direct_sw_radiation.copy()
            for col in total_sw_radiation.columns[1:]:  # Skip time column
                # Find matching column in diffuse data
                for diffuse_col in data.diffuse_sw_radiation.columns[1:]:
                    if col.split('(')[0] == diffuse_col.split('(')[0]:  # Match by name prefix
                        total_sw_radiation[col] = data.direct_sw_radiation[col] + data.diffuse_sw_radiation[diffuse_col]
                        break

            # Window left - Total
            process_and_validate(
                title="Gesamte kurzwellige Strahlung Fenster links",
                y_axis_label="Strahlung [W/m²]",
                output_dir=out_dir,
                case=case,
                variant=variant,
                year=year,
                data=data,
                nandrad_df=total_sw_radiation,
                nandrad_col_substr="Window left",
                ep_var="Surface Outside Face Incident Solar Radiation Rate per Area",
                ep_key="ZONE SUBSURFACE 1",
                trnsys_col="Tzone",  # placeholder
                trnsys_conv=0.,
                ep_conv=1.,
                nandrad_conv=1.,
                create_monthly_summary=True,
                unit="W/m²",
                ref_suffix="",
            )
            # Window right - Total
            process_and_validate(
                title="Gesamte kurzwellige Strahlung Fenster rechts",
                y_axis_label="Strahlung [W/m²]",
                output_dir=out_dir,
                case=case,
                variant=variant,
                year=year,
                data=data,
                nandrad_df=total_sw_radiation,
                nandrad_col_substr="Window right",
                ep_var="Surface Outside Face Incident Solar Radiation Rate per Area",
                ep_key="ZONE SUBSURFACE 2",
                trnsys_col="Tzone",  # placeholder
                trnsys_conv=0.,
                ep_conv=1.,
                nandrad_conv=1.,
                create_monthly_summary=True,
                unit="W/m²",
                ref_suffix="",
            )

        # --- Direct Short Wave Radiation on windows ---
        if data.direct_sw_radiation is not None:
            # Window left - Direct
            process_and_validate(
                title="Direkte kurzwellige Strahlung Fenster links",
                y_axis_label="Strahlung [W/m²]",
                output_dir=out_dir,
                case=case,
                variant=variant,
                year=year,
                data=data,
                nandrad_df=data.direct_sw_radiation,
                nandrad_col_substr="Window left",
                ep_var="Surface Outside Face Incident Beam Solar Radiation Rate per Area",
                ep_key="ZONE SUBSURFACE 1",
                trnsys_col="Tzone",
                trnsys_conv=0.,
                ep_conv=1.,
                nandrad_conv=1.,
                create_monthly_summary=True,
                unit="W/m²",
                ref_suffix="",
            )
            # Window right - Direct
            process_and_validate(
                title="Direkte kurzwellige Strahlung Fenster rechts",
                y_axis_label="Strahlung [W/m²]",
                output_dir=out_dir,
                case=case,
                variant=variant,
                year=year,
                data=data,
                nandrad_df=data.direct_sw_radiation,
                nandrad_col_substr="Window right",
                ep_var="Surface Outside Face Incident Beam Solar Radiation Rate per Area",
                ep_key="ZONE SUBSURFACE 2",
                trnsys_col="Tzone",
                trnsys_conv=0.,
                ep_conv=1.,
                nandrad_conv=1.,
                create_monthly_summary=True,
                unit="W/m²",
                ref_suffix="",
            )

        # --- Diffuse Short Wave Radiation on windows (Sky + Ground) ---
        if data.diffuse_sw_radiation is not None:
            # Window left - Diffuse
            process_and_validate(
                title="Diffuse kurzwellige Strahlung Fenster links",
                y_axis_label="Strahlung [W/m²]",
                output_dir=out_dir,
                case=case,
                variant=variant,
                year=year,
                data=data,
                nandrad_df=data.diffuse_sw_radiation,
                nandrad_col_substr="Window left",
                ep_var="Surface Outside Face Incident Sky Diffuse Solar Radiation Rate per Area",
                ep_key="ZONE SUBSURFACE 1",
                trnsys_col="Tzone",
                trnsys_conv=0.,
                ep_conv=1.,
                nandrad_conv=1.,
                create_monthly_summary=True,
                unit="W/m²",
                ref_suffix="",
            )
            # Window right - Diffuse
            process_and_validate(
                title="Diffuse kurzwellige Strahlung Fenster rechts",
                y_axis_label="Strahlung [W/m²]",
                output_dir=out_dir,
                case=case,
                variant=variant,
                year=year,
                data=data,
                nandrad_df=data.diffuse_sw_radiation,
                nandrad_col_substr="Window right",
                ep_var="Surface Outside Face Incident Sky Diffuse Solar Radiation Rate per Area",
                ep_key="ZONE SUBSURFACE 2",
                trnsys_col="Tzone",
                trnsys_conv=0.,
                ep_conv=1.,
                nandrad_conv=1.,
                create_monthly_summary=True,
                unit="W/m²",
                ref_suffix="",
            )

        # ==========================================================
        # ASHRAE 140 Reference Checking
        # ==========================================================
        is_ff = case.upper().endswith("FF")

        if annual_refs is not None:
            if is_ff and df_air_temp is not None:
                # Free-float cases: check temperature extremes
                nandrad_temps = df_air_temp["NANDRAD"]
                validation_results.extend(check_free_float_references(
                    nandrad_temp_max=float(nandrad_temps.max()),
                    nandrad_temp_min=float(nandrad_temps.min()),
                    nandrad_temp_avg=float(nandrad_temps.mean()),
                    case=case,
                    ff_refs=annual_refs.free_float,
                ))
            else:
                # Non-FF cases: check annual heating/cooling totals and peaks
                if df_heating is not None:
                    annual_heating_kwh = float(df_heating["NANDRAD"].sum())
                    peak_heating_kw = float(df_heating["NANDRAD"].max())
                else:
                    annual_heating_kwh = 0.0
                    peak_heating_kw = 0.0

                if df_cooling is not None:
                    annual_cooling_kwh = float(df_cooling["NANDRAD"].sum())
                    peak_cooling_kw = float(df_cooling["NANDRAD"].max())
                else:
                    annual_cooling_kwh = 0.0
                    peak_cooling_kw = 0.0

                validation_results.extend(check_annual_references(
                    nandrad_annual_heating_kwh=annual_heating_kwh,
                    nandrad_annual_cooling_kwh=annual_cooling_kwh,
                    case=case,
                    annual_refs=annual_refs.annual,
                ))
                validation_results.extend(check_peak_references(
                    nandrad_peak_heating_kw=peak_heating_kw,
                    nandrad_peak_cooling_kw=peak_cooling_kw,
                    case=case,
                    annual_refs=annual_refs.annual,
                ))

        # Generate validation summary report
        if validation_results:
            generate_validation_report(
                results=validation_results,
                output_dir=out_dir,
                case=case,
                variant=variant,
            )

        logging.info("%s%sValidation finished successfully!%s", Ansi.OKGREEN, Ansi.BOLD, Ansi.ENDC)
        logging.info("Results: %s", out_dir)
        return 0

    except FileNotFoundError as e:
        logging.error("%sMissing file/executable: %s%s", Ansi.FAIL, e, Ansi.ENDC)
    except subprocess.CalledProcessError as e:
        logging.error("%sSimulation failed. Command '%s' returned %s%s",
                      Ansi.FAIL, " ".join(e.cmd), e.returncode, Ansi.ENDC)
    except Exception as e:
        logging.error("%sUnexpected error: %s%s", Ansi.FAIL, e, Ansi.ENDC, exc_info=True)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
