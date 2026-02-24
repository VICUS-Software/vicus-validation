# BESTEST Validation Suite

ASHRAE 140 (BESTEST) Validierung thermischer Simulationsergebnisse von **NANDRAD**, **EnergyPlus v9.0.1** und **TRNSYS**.

## Ergebnisse

**[Gesamtübersicht (HTML)](validation_results/overview_report.html)** | [Gesamtübersicht (TSV)](validation_results/overview_report.tsv)

### Einzelergebnisse nach Testfall

| Case | Beschreibung | Ergebnisse |
|------|-------------|------------|
| [600](validation_results/Case600_v1/) | Basisfall, Leichtbau, Südfenster | [Report](validation_results/Case600_v1/Case600_v1_validation_report.html) |
| [600FF](validation_results/Case600FF_v1/) | Basisfall, Free-Float | [Report](validation_results/Case600FF_v1/Case600FF_v1_validation_report.html) |
| [610](validation_results/Case610_v1/) | Süd-Verschattung | [Report](validation_results/Case610_v1/Case610_v1_validation_report.html) |
| [620](validation_results/Case620_v1/) | Ost-/West-Fenster | [Report](validation_results/Case620_v1/Case620_v1_validation_report.html) |
| [630](validation_results/Case630_v1/) | Ost-/West-Verschattung | [Report](validation_results/Case630_v1/Case630_v1_validation_report.html) |
| [640](validation_results/Case640_v1/) | Nachtlüftung | [Report](validation_results/Case640_v1/Case640_v1_validation_report.html) |
| [650](validation_results/Case650_v1/) | Kein Heizen | [Report](validation_results/Case650_v1/Case650_v1_validation_report.html) |
| [650FF](validation_results/Case650FF_v1/) | Kein Heizen, Free-Float | [Report](validation_results/Case650FF_v1/Case650FF_v1_validation_report.html) |
| [660](validation_results/Case660_v1/) | Niedrige Lüftung | [Report](validation_results/Case660_v1/Case660_v1_validation_report.html) |
| [670](validation_results/Case670_v1/) | Einzelscheibenverglasung | [Report](validation_results/Case670_v1/Case670_v1_validation_report.html) |
| [680](validation_results/Case680_v1/) | Erhöhte Isolation | [Report](validation_results/Case680_v1/Case680_v1_validation_report.html) |
| [680FF](validation_results/Case680FF_v1/) | Erhöhte Isolation, Free-Float | [Report](validation_results/Case680FF_v1/Case680FF_v1_validation_report.html) |
| [685](validation_results/Case685_v1/) | 685 | [Report](validation_results/Case685_v1/Case685_v1_validation_report.html) |
| [695](validation_results/Case695_v1/) | 695 | [Report](validation_results/Case695_v1/Case695_v1_validation_report.html) |
| [900](validation_results/Case900_v1/) | Basisfall, Schwerbau | [Report](validation_results/Case900_v1/Case900_v1_validation_report.html) |
| [900FF](validation_results/Case900FF_v1/) | Schwerbau, Free-Float | [Report](validation_results/Case900FF_v1/Case900FF_v1_validation_report.html) |
| [910](validation_results/Case910_v1/) | Süd-Verschattung, Schwerbau | [Report](validation_results/Case910_v1/Case910_v1_validation_report.html) |
| [920](validation_results/Case920_v1/) | Ost-/West-Fenster, Schwerbau | [Report](validation_results/Case920_v1/Case920_v1_validation_report.html) |
| [930](validation_results/Case930_v1/) | Ost-/West-Verschattung, Schwerbau | [Report](validation_results/Case930_v1/Case930_v1_validation_report.html) |
| [940](validation_results/Case940_v1/) | Nachtlüftung, Schwerbau | [Report](validation_results/Case940_v1/Case940_v1_validation_report.html) |
| [950](validation_results/Case950_v1/) | Kein Heizen, Schwerbau | [Report](validation_results/Case950_v1/Case950_v1_validation_report.html) |
| [950FF](validation_results/Case950FF_v1/) | Kein Heizen, Schwerbau, Free-Float | [Report](validation_results/Case950FF_v1/Case950FF_v1_validation_report.html) |
| [960](validation_results/Case960_v1/) | Sunspace | [Report](validation_results/Case960_v1/Case960_v1_validation_report.html) |
| [980](validation_results/Case980_v1/) | 980 | [Report](validation_results/Case980_v1/Case980_v1_validation_report.html) |
| [980FF](validation_results/Case980FF_v1/) | 980 Free-Float | [Report](validation_results/Case980FF_v1/Case980FF_v1_validation_report.html) |
| [985](validation_results/Case985_v1/) | 985 | [Report](validation_results/Case985_v1/Case985_v1_validation_report.html) |
| [995](validation_results/Case995_v1/) | 995 | [Report](validation_results/Case995_v1/Case995_v1_validation_report.html) |

## Validierung ausführen

```bash
source .venv/bin/activate

# Alle Cases:
python run_all_validations.py --nandrad-exec /path/to/NandradSolver

# Einzelner Case:
python validate_nandrad.py -c="600" -v="v1" -w="ZONE SUBSURFACE 1,ZONE SUBSURFACE 2"

# Nur Auswertung (ohne Simulation):
python run_all_validations.py --skip-run
```

## Ausgaben pro Testfall

Jeder Testfall erzeugt im Ordner `validation_results/Case{N}_{variant}/`:

| Datei | Inhalt |
|-------|--------|
| `*_validation_report.html` | Pass/Fail-Übersicht gegen ASHRAE-Referenzen |
| `*_hourly.html` | Interaktiver Stundenvergleich (Plotly) |
| `*_monthly_mean.svg` | Monatliche Energiesummen mit Referenzbändern |
| `*_monthly_max.svg` | Monatliche Spitzenlasten |
| `*_hourly.tsv` | Stundenwerte als TSV |
| `*_monthly_sum.tsv` | Monatssummen |
| `*_yearly_sum.tsv` | Jahressummen |

## Simulationsengines

- **NANDRAD** - TSV-Ausgaben, Solver unter `bin/NandradSolver`
- **EnergyPlus v9.0.1** - ESO-Binärausgaben
- **TRNSYS** - Whitespace-getrennte `.out`-Dateien
