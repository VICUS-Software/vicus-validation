#!/usr/bin/env python3
"""Comprehensive BESTEST energy balance comparison figure.

Reads existing hourly TSV outputs and raw simulation data to produce
a multi-panel Matplotlib figure comparing NANDRAD, EnergyPlus, and TRNSYS.

Usage:
    source .venv/bin/activate
    python plot_case600_comparison.py                     # Case 600 v1
    python plot_case600_comparison.py -c 900 -v v1        # single case
    python plot_case600_comparison.py --all                # all cases
"""

import argparse
import glob as globmod
import os
import sys
import locale
import datetime as dt

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DATA_DIR = "data"
REF_DIR = os.path.join(DATA_DIR, "reference")

COLORS = {
    "NANDRAD":    "#1f77b4",
    "EnergyPlus": "#ff7f0e",
    "TRNSYS":     "#2ca02c",
}
ENGINES = list(COLORS.keys())

MONTH_LABELS = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
                "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]

# Monthly reference bands exist only for these cases
MONTHLY_REF_CASES = {"600", "900"}

try:
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
except locale.Error:
    pass


# ---------------------------------------------------------------------------
# I/O helpers  (use module-level RESULTS_DIR / TAG / CASE set by generate())
# ---------------------------------------------------------------------------
_ctx = {}  # mutable context dict set per-case


def _tsv_path(metric, suffix):
    return os.path.join(_ctx["results_dir"],
                        f"{_ctx['tag']}_{metric}_{suffix}.tsv")


def read_hourly(metric):
    path = _tsv_path(metric, "hourly")
    return pd.read_csv(path, sep="\t", parse_dates=["Datetime"],
                       index_col="Datetime")


def read_monthly_integral(metric):
    path = _tsv_path(metric, "monthly_integral")
    return pd.read_csv(path, sep="\t", index_col=0, parse_dates=True)


def read_yearly_sum(metric):
    path = _tsv_path(metric, "yearly_sum")
    df = pd.read_csv(path, sep="\t", index_col=0)
    return df.iloc[0]


def read_global_max(metric):
    path = _tsv_path(metric, "hourly_global_max")
    return pd.read_csv(path, sep="\t")


def read_monthly_refs():
    path = os.path.join(REF_DIR, "monthly-references.tsv")
    return pd.read_csv(path, sep="\t", index_col="Month")


def read_annual_refs():
    path = os.path.join(REF_DIR, "annual-references.tsv")
    return pd.read_csv(path, sep="\t", index_col="Case")


def read_ff_refs():
    path = os.path.join(REF_DIR, "free-float-references.tsv")
    return pd.read_csv(path, sep="\t", index_col="Case")


def read_nandrad_ventilation():
    path = os.path.join(DATA_DIR, "nandrad", _ctx["tag"], "results",
                        "VentilationHeatLoad-mean-Hourly.tsv")
    df = pd.read_csv(path, sep="\t")
    s = pd.to_numeric(df.iloc[:, 1], errors="coerce")
    idx = pd.date_range(start=dt.datetime(2021, 1, 1),
                        periods=len(s), freq="h")
    s.index = idx[:len(s)]
    return s


def read_ep_infiltration():
    try:
        import esoreader
    except ImportError:
        return None
    eso_path = os.path.join(DATA_DIR, "energyplus", "eplusout.eso")
    if not os.path.isfile(eso_path):
        return None
    eso = esoreader.read_from_path(eso_path)
    var_names = {v[2] for v in eso.dd.variables.values()}
    loss_var = "Zone Infiltration Sensible Heat Loss Energy"
    gain_var = "Zone Infiltration Sensible Heat Gain Energy"
    if loss_var not in var_names or gain_var not in var_names:
        return None
    J_TO_WH = 1.0 / 3600.0
    loss = eso.to_frame(loss_var, frequency="Hourly")
    gain = eso.to_frame(gain_var, frequency="Hourly")
    if isinstance(loss, pd.DataFrame):
        loss = loss.iloc[:, 0]
    if isinstance(gain, pd.DataFrame):
        gain = gain.iloc[:, 0]
    net_wh = (pd.to_numeric(gain, errors="coerce") -
              pd.to_numeric(loss, errors="coerce")) * J_TO_WH
    idx = pd.date_range(start=dt.datetime(2021, 1, 1),
                        periods=len(net_wh), freq="h")
    net_wh.index = idx[:len(net_wh)]
    return net_wh


# ---------------------------------------------------------------------------
# Plotting helpers
# ---------------------------------------------------------------------------

def _add_ref_band(ax, ref_min, ref_max, x_positions, width):
    for i, (lo, hi) in enumerate(zip(ref_min, ref_max)):
        ax.fill_between(
            [x_positions[i] - width * 2, x_positions[i] + width * 2],
            lo, hi, alpha=0.15, color="grey", zorder=0)
        ax.plot([x_positions[i] - width * 2, x_positions[i] + width * 2],
                [lo, lo], color="grey", lw=0.5, ls="--", zorder=0)
        ax.plot([x_positions[i] - width * 2, x_positions[i] + width * 2],
                [hi, hi], color="grey", lw=0.5, ls="--", zorder=0)


def grouped_bar(ax, df_monthly, title, ylabel, ref_min=None, ref_max=None,
                engines=None):
    if engines is None:
        engines = [e for e in ENGINES if e in df_monthly.columns]
    n_eng = len(engines)
    x = np.arange(12)
    width = 0.8 / max(n_eng, 1)
    if ref_min is not None and ref_max is not None:
        _add_ref_band(ax, ref_min, ref_max, x, width)
    for j, eng in enumerate(engines):
        vals = df_monthly[eng].values[:12]
        offset = (j - (n_eng - 1) / 2) * width
        ax.bar(x + offset, vals, width, label=eng, color=COLORS[eng],
               edgecolor="white", linewidth=0.3, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(MONTH_LABELS, fontsize=8)
    ax.set_title(title, fontsize=10, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=8)
    ax.legend(fontsize=7, loc="best")
    ax.grid(axis="y", alpha=0.3, zorder=0)
    ax.tick_params(labelsize=8)


def _safe_panel(ax, func, fallback_title):
    """Call func(ax); on failure show placeholder text."""
    try:
        func(ax)
    except Exception as e:
        ax.text(0.5, 0.5, f"Daten nicht verfügbar\n({e})",
                ha="center", va="center", transform=ax.transAxes,
                fontsize=8, color="grey")
        ax.set_title(fallback_title, fontsize=10, fontweight="bold")


# ---------------------------------------------------------------------------
# Panel builders
# ---------------------------------------------------------------------------

def panel_monthly_heating(ax):
    case = _ctx["case"]
    df = read_monthly_integral("Heizenergie")
    ref_min = ref_max = None
    if case in MONTHLY_REF_CASES:
        refs = read_monthly_refs()
        ref_min = refs[f"Case{case}_heating_min"].values
        ref_max = refs[f"Case{case}_heating_max"].values
    grouped_bar(ax, df, "Monatliche Heizenergie", "[kWh]",
                ref_min=ref_min, ref_max=ref_max)


def panel_monthly_cooling(ax):
    case = _ctx["case"]
    df = read_monthly_integral("Kühlenergie")
    ref_min = ref_max = None
    if case in MONTHLY_REF_CASES:
        refs = read_monthly_refs()
        ref_min = refs[f"Case{case}_cooling_min"].values
        ref_max = refs[f"Case{case}_cooling_max"].values
    grouped_bar(ax, df, "Monatliche Kühlenergie", "[kWh]",
                ref_min=ref_min, ref_max=ref_max)


def panel_air_temperature(ax):
    df = read_hourly("Lufttemperatur")
    for eng in ENGINES:
        if eng in df.columns:
            ax.plot(df.index, df[eng], label=eng, color=COLORS[eng],
                    lw=0.3, alpha=0.8)
    # Add free-float reference lines if applicable
    case = _ctx["case"]
    ff_key = case if case.endswith("FF") else None
    if ff_key is None and case == "960":
        ff_key = "960"
    if ff_key:
        try:
            ff = read_ff_refs().loc[ff_key]
            ax.axhline(ff["temp_max_min"], color="grey", ls=":", lw=0.8,
                       label=f"Ref Tmax [{ff['temp_max_min']:.1f}–{ff['temp_max_max']:.1f}]")
            ax.axhline(ff["temp_max_max"], color="grey", ls=":", lw=0.8)
            ax.axhline(ff["temp_min_min"], color="grey", ls="--", lw=0.8,
                       label=f"Ref Tmin [{ff['temp_min_min']:.1f}–{ff['temp_min_max']:.1f}]")
            ax.axhline(ff["temp_min_max"], color="grey", ls="--", lw=0.8)
        except Exception:
            pass
    ax.set_title("Lufttemperatur (stündlich)", fontsize=10, fontweight="bold")
    ax.set_ylabel("[°C]", fontsize=8)
    ax.legend(fontsize=6, loc="upper right")
    ax.grid(alpha=0.3)
    ax.tick_params(labelsize=7)
    ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b"))


def panel_ventilation(ax):
    engines_found = []
    monthly_data = {}
    try:
        s_nan = read_nandrad_ventilation().iloc[:8759]
        monthly_data["NANDRAD"] = s_nan.resample("ME").sum().abs() / 1000.0
        engines_found.append("NANDRAD")
    except Exception:
        pass
    s_ep = read_ep_infiltration()
    if s_ep is not None:
        s_ep = s_ep.iloc[:8759]
        monthly_data["EnergyPlus"] = s_ep.resample("ME").sum().abs() / 1000.0
        engines_found.append("EnergyPlus")
    if not engines_found:
        ax.text(0.5, 0.5, "Daten nicht verfügbar",
                ha="center", va="center", transform=ax.transAxes, fontsize=9)
        ax.set_title("Lüftungswärmeverluste", fontsize=10, fontweight="bold")
        return
    n_eng = len(engines_found)
    x = np.arange(12)
    width = 0.8 / n_eng
    for j, eng in enumerate(engines_found):
        vals = monthly_data[eng].values[:12]
        offset = (j - (n_eng - 1) / 2) * width
        ax.bar(x + offset, vals, width, label=eng, color=COLORS[eng],
               edgecolor="white", linewidth=0.3, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(MONTH_LABELS, fontsize=8)
    note = "" if n_eng > 1 else f" (nur {engines_found[0]})"
    ax.set_title(f"Lüftungs-/Infiltrationswärmeverluste{note}",
                 fontsize=10, fontweight="bold")
    ax.set_ylabel("[kWh]", fontsize=8)
    ax.legend(fontsize=7)
    ax.grid(axis="y", alpha=0.3, zorder=0)
    ax.tick_params(labelsize=8)


def panel_transmitted_solar(ax):
    df = read_monthly_integral(
        "Transmittierte_kurzwellige_Strahlung_Fenster") / 1000.0
    grouped_bar(ax, df, "Transmittierte Solarstrahlung Fenster", "[kWh/m²]")


def panel_radiation_by_orientation(ax):
    orientations = {"Nord": "Nord", "Ost": "Ost", "Süd": "Süd",
                    "West": "West", "Horiz.": "Horizontal"}
    data = {eng: [] for eng in ENGINES}
    labels = []
    for label, file_key in orientations.items():
        try:
            s = read_yearly_sum(f"Kurzwellige_Strahlungslasten_{file_key}")
        except Exception:
            continue
        labels.append(label)
        for eng in ENGINES:
            data[eng].append(s.get(eng, 0.0) / 1000.0)
    if not labels:
        ax.text(0.5, 0.5, "Daten nicht verfügbar", ha="center", va="center",
                transform=ax.transAxes, fontsize=9)
        ax.set_title("Solarstrahlung nach Orientierung", fontsize=10,
                     fontweight="bold")
        return
    n_eng = len(ENGINES)
    x = np.arange(len(labels))
    width = 0.8 / n_eng
    for j, eng in enumerate(ENGINES):
        offset = (j - (n_eng - 1) / 2) * width
        ax.bar(x + offset, data[eng], width, label=eng, color=COLORS[eng],
               edgecolor="white", linewidth=0.3, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_title("Einfallende Solarstrahlung nach Orientierung (jährlich)",
                 fontsize=10, fontweight="bold")
    ax.set_ylabel("[kWh/m²]", fontsize=8)
    ax.legend(fontsize=7)
    ax.grid(axis="y", alpha=0.3, zorder=0)
    ax.tick_params(labelsize=8)


def panel_window_conduction(ax):
    # Discover all window conduction files for this case
    pattern = os.path.join(_ctx["results_dir"],
                           f"{_ctx['tag']}_Wärmeleitung_Fenster_*_hourly.tsv")
    files = sorted(globmod.glob(pattern))
    if not files:
        raise FileNotFoundError("No window conduction files found")
    # Read and sum all windows
    df = None
    for f in files:
        tmp = pd.read_csv(f, sep="\t", parse_dates=["Datetime"],
                          index_col="Datetime")
        df = tmp if df is None else df.add(tmp, fill_value=0.0)
    monthly = df.resample("ME").sum() / 1000.0
    engines = [e for e in ENGINES
               if e in monthly.columns and monthly[e].abs().sum() > 0.01]
    if not engines:
        engines = [e for e in ENGINES if e in monthly.columns]
    n_win = len(files)
    title = ("Fenster-Wärmeleitung" if n_win == 1
             else f"Fenster-Wärmeleitung ({n_win} Fenster)")
    grouped_bar(ax, monthly, title, "[kWh]", engines=engines)


def panel_monthly_radiation_south(ax):
    df = read_monthly_integral("Kurzwellige_Strahlungslasten_Süd") / 1000.0
    grouped_bar(ax, df, "Einfallende Solarstrahlung Süd (monatlich)",
                "[kWh/m²]")


def panel_annual_balance(ax):
    case = _ctx["case"]
    case_num = case.rstrip("F")  # strip FF suffix for ref lookup
    # Strip remaining F for case numbers like "600F" -> "600"
    case_num = case_num.rstrip("F")

    heat_yr = read_yearly_sum("Heizenergie")
    cool_yr = read_yearly_sum("Kühlenergie")
    heat_max = read_global_max("Heizenergie")
    cool_max = read_global_max("Kühlenergie")

    categories = ["Heizenergie\n[MWh]", "Kühlenergie\n[MWh]",
                  "Heiz-Spitze\n[kW]", "Kühl-Spitze\n[kW]"]
    data = {}
    for eng in ENGINES:
        h_yr = heat_yr.get(eng, 0.0) / 1000.0
        c_yr = cool_yr.get(eng, 0.0) / 1000.0
        h_pk_row = heat_max.loc[heat_max["Series"] == eng]
        c_pk_row = cool_max.loc[cool_max["Series"] == eng]
        h_pk = float(h_pk_row["MaxValue"].values[0]) if len(h_pk_row) else 0.0
        c_pk = float(c_pk_row["MaxValue"].values[0]) if len(c_pk_row) else 0.0
        data[eng] = [h_yr, c_yr, h_pk, c_pk]

    # Reference bounds (only for cases in annual-references.tsv)
    ref_bounds = None
    try:
        annual_refs = read_annual_refs()
        if int(case_num) in annual_refs.index:
            ref = annual_refs.loc[int(case_num)]
            ref_bounds = [
                (ref["heating_min"], ref["heating_max"]),
                (ref["cooling_min"], ref["cooling_max"]),
                (ref["peak_heating_min"], ref["peak_heating_max"]),
                (ref["peak_cooling_min"], ref["peak_cooling_max"]),
            ]
    except Exception:
        pass

    n_cat = len(categories)
    n_eng = len(ENGINES)
    x = np.arange(n_cat)
    width = 0.8 / n_eng

    if ref_bounds:
        for i, (lo, hi) in enumerate(ref_bounds):
            ax.fill_between(
                [x[i] - width * 2, x[i] + width * 2],
                lo, hi, alpha=0.15, color="grey", zorder=0)
            ax.plot([x[i] - width * 2, x[i] + width * 2],
                    [lo, lo], color="grey", lw=0.5, ls="--", zorder=0)
            ax.plot([x[i] - width * 2, x[i] + width * 2],
                    [hi, hi], color="grey", lw=0.5, ls="--", zorder=0)

    for j, eng in enumerate(ENGINES):
        offset = (j - (n_eng - 1) / 2) * width
        bars = ax.bar(x + offset, data[eng], width, label=eng,
                      color=COLORS[eng], edgecolor="white", linewidth=0.3,
                      zorder=3)
        for bar_rect, val in zip(bars, data[eng]):
            ax.text(bar_rect.get_x() + bar_rect.get_width() / 2,
                    bar_rect.get_height(), f"{val:.2f}",
                    ha="center", va="bottom", fontsize=6, rotation=45)

    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_title(f"Jährliche Energiebilanz — Case {case}",
                 fontsize=11, fontweight="bold")
    ax.set_ylabel("MWh / kW", fontsize=9)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(axis="y", alpha=0.3, zorder=0)
    ax.tick_params(labelsize=8)
    if ref_bounds:
        ax.text(0.01, 0.97, "Grau = BESTEST Referenzbereich",
                transform=ax.transAxes, fontsize=7, color="grey",
                va="top", ha="left")


# ---------------------------------------------------------------------------
# Main figure generation
# ---------------------------------------------------------------------------

def generate(case, variant, open_result=False):
    """Generate the comprehensive comparison for one case/variant."""
    tag = f"Case{case}_{variant}"
    results_dir = os.path.join("validation_results", tag)
    if not os.path.isdir(results_dir):
        print(f"SKIP: {results_dir} not found")
        return False

    # Set module context
    _ctx["case"] = case
    _ctx["variant"] = variant
    _ctx["tag"] = tag
    _ctx["results_dir"] = results_dir

    fig, axes = plt.subplots(5, 2, figsize=(20, 22))
    fig.suptitle(f"BESTEST Case {case} — Umfassender Simulationsvergleich\n"
                 f"NANDRAD / EnergyPlus v9.0.1 / TRNSYS",
                 fontsize=14, fontweight="bold", y=0.995)

    # Row 0: Heating & Cooling monthly
    _safe_panel(axes[0, 0], panel_monthly_heating, "Monatliche Heizenergie")
    _safe_panel(axes[0, 1], panel_monthly_cooling, "Monatliche Kühlenergie")

    # Row 1: Air temperature & Ventilation
    _safe_panel(axes[1, 0], panel_air_temperature, "Lufttemperatur")
    _safe_panel(axes[1, 1], panel_ventilation, "Lüftungswärmeverluste")

    # Row 2: Transmitted solar & Radiation by orientation
    _safe_panel(axes[2, 0], panel_transmitted_solar,
                "Transmittierte Solarstrahlung")
    _safe_panel(axes[2, 1], panel_radiation_by_orientation,
                "Solarstrahlung nach Orientierung")

    # Row 3: Window conduction & South radiation monthly
    _safe_panel(axes[3, 0], panel_window_conduction, "Fenster-Wärmeleitung")
    _safe_panel(axes[3, 1], panel_monthly_radiation_south,
                "Solarstrahlung Süd")

    # Row 4: Annual energy balance (spanning full width)
    axes[4, 0].remove()
    axes[4, 1].remove()
    gs = axes[0, 0].get_gridspec()
    ax_bottom = fig.add_subplot(gs[4, :])
    _safe_panel(ax_bottom, panel_annual_balance, "Jährliche Energiebilanz")

    fig.tight_layout(rect=[0, 0, 1, 0.97])

    base = os.path.join(results_dir, f"{tag}_comprehensive_comparison")
    fig.savefig(f"{base}.svg", bbox_inches="tight")
    fig.savefig(f"{base}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"OK   {tag}")

    if open_result:
        try:
            import subprocess
            subprocess.Popen(["xdg-open", f"{base}.png"],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        except Exception:
            pass
    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate comprehensive BESTEST comparison figures.")
    parser.add_argument("-c", "--case", default="600",
                        help="Case number (e.g., 600, 600FF, 950)")
    parser.add_argument("-v", "--variant", default="v1",
                        help="Variant (e.g., v1, v2)")
    parser.add_argument("--all", action="store_true",
                        help="Generate for all existing validation results")
    parser.add_argument("--open", action="store_true",
                        help="Open result with xdg-open")
    args = parser.parse_args()

    if args.all:
        # Discover all Case*_v*/ directories
        dirs = sorted(globmod.glob("validation_results/Case*_v*/"))
        if not dirs:
            print("ERROR: No validation_results/Case*_v*/ found.")
            sys.exit(1)
        ok = fail = 0
        for d in dirs:
            name = os.path.basename(d.rstrip("/"))
            # Parse CaseXXX_vN
            parts = name.rsplit("_", 1)
            if len(parts) != 2:
                continue
            case = parts[0].replace("Case", "")
            variant = parts[1]
            if generate(case, variant):
                ok += 1
            else:
                fail += 1
        print(f"\nDone: {ok} generated, {fail} skipped.")
    else:
        if not generate(args.case, args.variant, open_result=args.open):
            sys.exit(1)


if __name__ == "__main__":
    main()
