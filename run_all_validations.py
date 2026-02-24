#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Batch runner for BESTEST validation suite.

Discovers all available NANDRAD test cases, runs validate_nandrad.py for each,
collects per-case validation reports, and generates an overview report (TSV + HTML).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import logging
from pathlib import Path
from typing import Optional, Sequence

import pandas as pd


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )


# ---------------------------------------------------------------------------
# Case discovery
# ---------------------------------------------------------------------------

def discover_cases(data_dir: Path, variant: str) -> list[str]:
    """Glob for Case*_{variant}.nandrad and extract sorted case numbers."""
    pattern = f"Case*_{variant}.nandrad"
    files = sorted(data_dir.joinpath("nandrad").glob(pattern))

    regex = re.compile(rf"Case(\d+(?:FF)?)_{re.escape(variant)}\.nandrad$")
    cases: list[str] = []
    for f in files:
        m = regex.match(f.name)
        if m:
            cases.append(m.group(1))

    # Natural sort: numeric part first, then FF suffix
    def _sort_key(c: str) -> tuple[int, str]:
        m2 = re.match(r"(\d+)(FF)?", c)
        return (int(m2.group(1)), m2.group(2) or "") if m2 else (0, c)

    cases.sort(key=_sort_key)
    return cases


# ---------------------------------------------------------------------------
# Per-case execution
# ---------------------------------------------------------------------------

def run_single_case(
    case: str,
    variant: str,
    windows: str,
    nandrad_exec: Path,
    skip_run: bool,
    out_dir: Path,
    data_dir: Path,
) -> tuple[str, int, str]:
    """Run validate_nandrad.py for one case. Returns (case, returncode, stderr)."""
    cmd = [
        sys.executable, "validate_nandrad.py",
        f"-c={case}",
        f"-v={variant}",
        f"-w={windows}",
        f"--nandrad-exec={nandrad_exec}",
        f"--out-dir={out_dir}",
        f"--data-dir={data_dir}",
    ]
    if skip_run:
        cmd.append("--skip-run")

    logging.info("Running Case %s ...", case)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logging.warning("Case %s exited with code %d", case, result.returncode)
        if result.stderr:
            # Show last few lines of stderr
            for line in result.stderr.strip().splitlines()[-5:]:
                logging.warning("  stderr: %s", line)
    else:
        logging.info("Case %s finished successfully.", case)
    return case, result.returncode, result.stderr


# ---------------------------------------------------------------------------
# Result collection
# ---------------------------------------------------------------------------

def collect_results(
    cases: list[str],
    variant: str,
    out_dir: Path,
    exit_codes: dict[str, int],
) -> pd.DataFrame:
    """Read per-case validation_report.tsv files into a combined DataFrame."""
    rows: list[dict] = []
    for case in cases:
        report_path = out_dir / f"Case{case}_{variant}" / f"Case{case}_{variant}_validation_report.tsv"
        if not report_path.exists():
            # Case had an error or produced no report
            rows.append({
                "Case": case,
                "Metrik": "(keine Ergebnisse)",
                "NANDRAD": "",
                "Ref Min": "",
                "Ref Max": "",
                "Status": "ERROR" if exit_codes.get(case, 1) != 0 else "N/A",
            })
            continue
        try:
            df = pd.read_csv(report_path, sep="\t")
            for _, row in df.iterrows():
                rows.append({
                    "Case": case,
                    "Metrik": row.get("Metrik", ""),
                    "NANDRAD": row.get("NANDRAD", ""),
                    "Ref Min": row.get("Ref Min", ""),
                    "Ref Max": row.get("Ref Max", ""),
                    "Status": row.get("Status", "N/A"),
                })
        except Exception as exc:
            logging.warning("Failed to read report for Case %s: %s", case, exc)
            rows.append({
                "Case": case,
                "Metrik": "(Fehler beim Lesen)",
                "NANDRAD": "",
                "Ref Min": "",
                "Ref Max": "",
                "Status": "ERROR",
            })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Overview report generation
# ---------------------------------------------------------------------------

def build_summary(combined: pd.DataFrame) -> pd.DataFrame:
    """Build per-case summary: total metrics, pass, fail, n/a counts."""
    rows: list[dict] = []
    for case, grp in combined.groupby("Case", sort=False):
        n_total = len(grp)
        n_pass = (grp["Status"] == "PASS").sum()
        n_fail = (grp["Status"] == "FAIL").sum()
        n_skip = grp["Status"].isin(["SKIP", "N/A"]).sum()
        n_error = (grp["Status"] == "ERROR").sum()
        if n_error > 0:
            result = "ERROR"
        elif n_fail > 0:
            result = "FAIL"
        else:
            result = "PASS"
        rows.append({
            "Case": case,
            "Metriken": n_total,
            "PASS": n_pass,
            "FAIL": n_fail,
            "SKIP/N/A": n_skip + n_error,
            "Ergebnis": result,
        })
    return pd.DataFrame(rows)


def write_overview_tsv(combined: pd.DataFrame, path: Path) -> None:
    combined.to_csv(path, sep="\t", index=False)
    logging.info("Overview TSV: %s", path)


def write_overview_html(
    combined: pd.DataFrame,
    summary: pd.DataFrame,
    path: Path,
    variant: str,
) -> None:
    """Generate a self-contained HTML overview report."""

    total_cases = len(summary)
    total_pass = (summary["Ergebnis"] == "PASS").sum()
    total_fail = (summary["Ergebnis"] == "FAIL").sum()
    total_error = (summary["Ergebnis"] == "ERROR").sum()

    def _result_color(val: str) -> str:
        if val == "PASS":
            return "#155724"
        if val == "FAIL":
            return "#721c24"
        return "#856404"

    def _result_bg(val: str) -> str:
        if val == "PASS":
            return "#d4edda"
        if val == "FAIL":
            return "#f8d7da"
        return "#fff3cd"

    def _status_bg(val: str) -> str:
        if val == "PASS":
            return "#d4edda"
        if val == "FAIL":
            return "#f8d7da"
        if val in ("SKIP", "N/A"):
            return "#e2e3e5"
        return "#fff3cd"

    # Summary table rows
    summary_rows = []
    for _, row in summary.iterrows():
        res = row["Ergebnis"]
        bg = _result_bg(res)
        clr = _result_color(res)
        summary_rows.append(
            f'<tr>'
            f'<td><a href="#case-{row["Case"]}">{row["Case"]}</a></td>'
            f'<td>{row["Metriken"]}</td>'
            f'<td>{row["PASS"]}</td>'
            f'<td>{row["FAIL"]}</td>'
            f'<td>{row["SKIP/N/A"]}</td>'
            f'<td style="background:{bg};color:{clr};font-weight:bold;">{res}</td>'
            f'</tr>'
        )

    # Per-case detail sections
    detail_sections = []
    for case, grp in combined.groupby("Case", sort=False):
        case_res = summary.loc[summary["Case"] == case, "Ergebnis"].iloc[0]
        res_bg = _result_bg(case_res)
        res_clr = _result_color(case_res)

        metric_rows = []
        for _, row in grp.iterrows():
            st = str(row["Status"])
            bg = _status_bg(st)
            metric_rows.append(
                f'<tr>'
                f'<td>{row["Metrik"]}</td>'
                f'<td>{row["NANDRAD"]}</td>'
                f'<td>{row["Ref Min"]}</td>'
                f'<td>{row["Ref Max"]}</td>'
                f'<td style="background:{bg};font-weight:bold;">{st}</td>'
                f'</tr>'
            )

        detail_sections.append(f"""
<details id="case-{case}">
<summary style="cursor:pointer;font-size:1.15em;margin:12px 0 4px;">
  Case {case}
  <span style="background:{res_bg};color:{res_clr};padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.9em;">{case_res}</span>
</summary>
<table>
<thead><tr><th>Metrik</th><th>NANDRAD</th><th>Ref Min</th><th>Ref Max</th><th>Status</th></tr></thead>
<tbody>
{"".join(metric_rows)}
</tbody>
</table>
</details>""")

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>BESTEST Validation Overview ({variant})</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; color: #333; }}
h1 {{ margin-bottom: 4px; }}
.subtitle {{ color: #666; margin-bottom: 20px; }}
.stats {{ font-size: 1.1em; margin: 12px 0 20px; }}
.stats span {{ font-weight: bold; }}
.pass {{ color: #155724; }}
.fail {{ color: #721c24; }}
.error {{ color: #856404; }}
table {{ border-collapse: collapse; width: 100%; margin-bottom: 8px; }}
th, td {{ border: 1px solid #ccc; padding: 6px 10px; text-align: left; }}
th {{ background: #f0f0f0; }}
tr:hover {{ background: #f9f9f9; }}
a {{ color: #0056b3; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
details {{ margin-bottom: 4px; }}
details > table {{ margin-top: 4px; }}
</style>
</head>
<body>
<h1>BESTEST Validation Overview</h1>
<p class="subtitle">Variante: {variant} &mdash; {total_cases} Testfälle</p>
<p class="stats">
  <span class="pass">{total_pass} PASS</span> &nbsp;|&nbsp;
  <span class="fail">{total_fail} FAIL</span> &nbsp;|&nbsp;
  <span class="error">{total_error} ERROR</span>
</p>

<h2>Zusammenfassung</h2>
<table>
<thead><tr><th>Case</th><th>Metriken</th><th>PASS</th><th>FAIL</th><th>SKIP/N/A</th><th>Ergebnis</th></tr></thead>
<tbody>
{"".join(summary_rows)}
</tbody>
</table>

<h2>Details</h2>
{"".join(detail_sections)}
</body>
</html>"""

    path.write_text(html, encoding="utf-8")
    logging.info("Overview HTML: %s", path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run all BESTEST validations and generate an overview report."
    )
    parser.add_argument("--skip-run", action="store_true",
                        help="Skip solver execution; only collect existing results")
    parser.add_argument("--cases", default=None,
                        help="Comma-separated case filter (e.g. 600,685,900)")
    parser.add_argument("--variant", default="v1", help="Variant to run (default: v1)")
    parser.add_argument("-w", "--windows",
                        default="ZONE SUBSURFACE 1,ZONE SUBSURFACE 2",
                        help="Default EnergyPlus window surface keys")
    parser.add_argument("--nandrad-exec", type=Path,
                        default=Path.cwd() / "bin" / "NandradSolver",
                        help="Path to NandradSolver executable")
    parser.add_argument("--data-dir", type=Path,
                        default=Path.cwd() / "data",
                        help="Root data directory")
    parser.add_argument("--out-dir", type=Path,
                        default=Path.cwd() / "validation_results",
                        help="Output directory")
    return parser.parse_args(argv)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: Optional[Sequence[str]] = None) -> int:
    setup_logging()
    args = parse_args(argv)

    variant = args.variant
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Discover cases
    all_cases = discover_cases(args.data_dir, variant)
    if not all_cases:
        logging.error("No NANDRAD case files found in %s/nandrad/", args.data_dir)
        return 1

    # 2. Filter if requested
    if args.cases:
        requested = {c.strip() for c in args.cases.split(",")}
        cases = [c for c in all_cases if c in requested]
        missing = requested - set(cases)
        if missing:
            logging.warning("Cases not found: %s", ", ".join(sorted(missing)))
    else:
        cases = all_cases

    logging.info("Cases to process (%d): %s", len(cases), ", ".join(cases))

    # 3. Run each case
    exit_codes: dict[str, int] = {}
    for case in cases:
        case_id, rc, _ = run_single_case(
            case=case,
            variant=variant,
            windows=args.windows,
            nandrad_exec=args.nandrad_exec,
            skip_run=args.skip_run,
            out_dir=out_dir,
            data_dir=args.data_dir,
        )
        exit_codes[case_id] = rc

    # 4. Collect results
    combined = collect_results(cases, variant, out_dir, exit_codes)
    if combined.empty:
        logging.error("No validation results found.")
        return 1

    # 5. Build summary
    summary = build_summary(combined)

    # 6. Write reports
    write_overview_tsv(combined, out_dir / "overview_report.tsv")
    write_overview_html(combined, summary, out_dir / "overview_report.html", variant)

    # 7. Print summary to console
    n_pass = (summary["Ergebnis"] == "PASS").sum()
    n_fail = (summary["Ergebnis"] == "FAIL").sum()
    n_error = (summary["Ergebnis"] == "ERROR").sum()
    logging.info(
        "Done. %d cases: %d PASS, %d FAIL, %d ERROR",
        len(summary), n_pass, n_fail, n_error,
    )

    if n_fail > 0 or n_error > 0:
        # Print failing cases
        failing = summary[summary["Ergebnis"] != "PASS"]
        for _, row in failing.iterrows():
            logging.info(
                "  Case %s: %s (PASS=%d, FAIL=%d)",
                row["Case"], row["Ergebnis"], row["PASS"], row["FAIL"],
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
