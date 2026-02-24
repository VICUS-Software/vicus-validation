# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BESTEST (Building Energy Simulation Test) validation suite comparing thermal simulation outputs from three engines:
- **NANDRAD** (TSV outputs) - primary validation target
- **EnergyPlus v9.0.1** (ESO binary outputs)
- **TRNSYS** (whitespace-delimited `.out` files)

Test cases follow the BESTEST standard (Cases 600-950, including FF free-float variants). Each case has configuration variants (v1, v2, v3).

## Running Validations

Activate the venv first: `source .venv/bin/activate`

Single case:
```bash
python validate_nandrad.py -c="600" -v="v1" -w="ZONE SUBSURFACE 1,ZONE SUBSURFACE 2"
```

With custom NANDRAD solver path:
```bash
python validate_nandrad.py --nandrad-exec /path/to/NandradSolver -c="600" -v="v1" -w="ZONE SUBSURFACE 1,ZONE SUBSURFACE 2"
```

Skip re-running simulations (only read existing results and generate comparison outputs):
```bash
python validate_nandrad.py -c="600" -v="v1" --skip-run
```

Batch execution: `start_validation.sh` (Linux) or `start_validation.bat` (Windows).

### CLI Arguments

| Flag | Default | Purpose |
|------|---------|---------|
| `-c/--case` | `600` | BESTEST case number (600, 600FF, 610, ..., 950FF) |
| `-v/--variant` | `v2` | Configuration variant (v1, v2, v3) |
| `-y/--year` | `2021` | Calendar year for hourly datetime index |
| `-w/--windows` | `ZONE SUBSURFACE 1` | Comma-separated EnergyPlus window surface keys |
| `--skip-run` | false | Only validate, don't execute solvers |
| `--data-dir` | `./data` | Root data directory |
| `--out-dir` | `./validation_results` | Output directory |
| `--ep-exec` | platform-dependent | EnergyPlus executable path |
| `--nandrad-exec` | `./bin/NandradSolver` | NANDRAD solver path |

## Python Dependencies

- `pandas`, `numpy` - data handling
- `matplotlib` - SVG bar charts with reference bands
- `plotly` - interactive HTML time-series plots
- `esoreader` - EnergyPlus ESO file reader

## Architecture (validate_nandrad.py)

The script is ~1250 lines, organized in clear sections:

1. **Constants & Utils** (top) - unit conversion factors (`J_TO_KWH`, `W_TO_KW`), ANSI colors, logging setup
2. **I/O Layer** - `read_tsv()`, `read_trnsys_table()`, `read_reference()`, `load_all()` returning a frozen `LoadedData` dataclass
3. **Series Extraction** - `col_by_substring()` for NANDRAD columns, `eso_series()` for EnergyPlus, `trnsys_series()` for TRNSYS (note: TRNSYS data is shifted by 1 hour for alignment)
4. **Plotting & Export** - `save_hourly_outputs()` (TSV + Plotly HTML), `save_monthly_bar_with_ref()` (Matplotlib SVG with reference min/max overlays)
5. **Statistics** - `_save_max_points()`, `_save_min_points()`, `_save_mean_air_temperature()` for global and monthly extrema
6. **Core Validation** - `process_and_validate()` orchestrates loading, unit conversion, alignment, and export for a given metric
7. **Simulation Runners** - `run_energyplus()`, `run_nandrad()` via subprocess
8. **CLI** - `parse_args()` with argparse
9. **Main** (~600 lines) - calls `process_and_validate()` for ~40+ metrics: air temperature, heating/cooling loads, window radiation, surface radiation (all orientations), shading factors, etc.

### Data Flow

```
NANDRAD TSVs + EnergyPlus ESO + TRNSYS .out + Reference TSVs
    └──> load_all() ──> LoadedData (frozen dataclass)
         └──> process_and_validate() per metric
              └──> aligned hourly DataFrame (NANDRAD | EnergyPlus | TRNSYS)
                   └──> TSV + HTML chart + monthly SVG + statistics
```

### Key Conventions

- All three simulators are aligned to a shared hourly `DatetimeIndex` (8759 hours, non-leap year)
- NANDRAD columns found via substring matching (`col_by_substring`); must be unique
- EnergyPlus variables extracted by variable name + optional surface key
- TRNSYS data: Latin-1 encoded, first row dropped, shifted 1 hour forward
- Optional data (shading factors, imposed radiation) loaded conditionally without failing
- German locale attempted for month labels in charts; falls back to English
- Output labels use German (Lufttemperatur, Heizenergie, Kühlenergie, etc.)

## Directory Layout

```
data/
  climate/       # EPW weather files + NANDRAD .c6b climate files
  nandrad/       # .nandrad XML inputs + Case{N}_{variant}/ result folders
  energyplus/    # .idf inputs + eplusout.eso (shared output file)
  trnsys/        # CASE{N}.out output files
  reference/     # monthly-references.tsv, annual-*.tsv, free-float-*.tsv
bin/               # NandradSolver, energyplus-9.0.1 executables
validation_results/  # Generated outputs per case (TSV, HTML, SVG)
```

Note: `data/energyplus/eplusout.eso` is a single shared ESO file that gets overwritten on each EnergyPlus run. EnergyPlus must be re-run for each case before reading results if not using `--skip-run`.
