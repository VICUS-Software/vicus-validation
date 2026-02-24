# BESTEST Validation Suite

ASHRAE 140 (BESTEST) Validierung thermischer Simulationsergebnisse von **NANDRAD**, **EnergyPlus v9.0.1** und **TRNSYS**.

## Ergebnisse

**[Gesamtübersicht (HTML)](overview_report.html)** | [Gesamtübersicht (TSV)](overview_report.tsv)

### Leichtbau-Serie (Cases 600–695)

| Case | Beschreibung | Änderung ggü. Basisfall |
|------|-------------|------------------------|
| 600 | Leichtbau Basisfall | Südfenster 12 m², Thermostat 20/27 °C, 0.5 ach, 200 W int. Lasten |
| 600FF | Free-Float Leichtbau | Wie 600, keine Heizung/Kühlung |
| 610 | Süd-Verschattung | Wie 600 + horizontaler Überhang 1.0 m |
| 620 | Ost-/West-Fenster | Wie 600, 6 m² Ost + 6 m² West statt 12 m² Süd |
| 630 | Ost-/West-Verschattung | Wie 620 + Überhang und vertikale Lamellen |
| 640 | Nachtabsenkung | Wie 600 + Heizung Nachtabsenkung auf 10 °C (23:00–07:00) |
| 650 | Nachtlüftung | Wie 600, keine Heizung, mech. Lüftung 1700 m³/h (18:00–07:00) |
| 650FF | Free-Float Nachtlüftung | Wie 650 ohne HVAC |
| 660 | Low-E Verglasung | Wie 600, Low-E Argon-Verglasung |
| 670 | Einscheibenverglasung | Wie 600, Einscheiben-Klarverglasung |
| 680 | Erhöhte Dämmung | Wie 600, Wand 0.250 m / Dach 0.400 m Dämmung |
| 680FF | Free-Float erhöhte Dämmung | Wie 680 ohne HVAC |
| 685 | Thermostat 20/20 | Wie 600, Thermostat 20/20 °C (kein Totband) |
| 695 | Erhöhte Dämmung + 20/20 | Kombination Case 680 + Case 685 |

### Schwerbau-Serie (Cases 900–995)

| Case | Beschreibung | Änderung ggü. Basisfall |
|------|-------------|------------------------|
| 900 | Schwerbau Basisfall | Wie 600, Betonstein-Wände und Bodenplatte |
| 900FF | Free-Float Schwerbau | Wie 900 ohne HVAC |
| 910 | Schwerbau + Süd-Verschattung | Case 900 + Case 610 (Überhang) |
| 920 | Schwerbau + Ost-/West-Fenster | Case 900 + Case 620 |
| 930 | Schwerbau + Ost-/West-Verschattung | Case 900 + Case 630 |
| 940 | Schwerbau + Nachtabsenkung | Case 900 + Case 640 |
| 950 | Schwerbau + Nachtlüftung | Case 900 + Case 650; Masse speichert Nachtkühle |
| 950FF | Free-Float Schwerbau + Nachtlüftung | Wie 950 ohne HVAC |
| 960 | Wintergarten (Sunspace) | Zwei-Zonen: Hinterzone Leichtbau, Wintergarten Schwerbau |
| 980 | Schwerbau + erhöhte Dämmung | Case 900 + Case 680 |
| 980FF | Free-Float Schwerbau + Dämmung | Wie 980 ohne HVAC |
| 985 | Schwerbau + 20/20 | Case 900 + Case 685 |
| 995 | Schwerbau + Dämmung + 20/20 | Case 900 + Case 695 |

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
