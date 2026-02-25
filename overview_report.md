# BESTEST Validation Overview (v1)

**14 PASS** | **13 FAIL** | **0 ERROR** | 27 Testfalle

## Zusammenfassung

| Case | Beschreibung | Metriken | PASS | FAIL | SKIP | Ergebnis |
|------|-------------|----------|------|------|------|----------|
| 600 | Leichtbau Basisfall | 28 | 25 | 3 | 0 | **FAIL** |
| 600FF | Free-Float Leichtbau | 3 | 3 | 0 | 0 | PASS |
| 610 | Süd-Verschattung | 4 | 3 | 1 | 0 | **FAIL** |
| 620 | Ost-/West-Fenster | 4 | 3 | 1 | 0 | **FAIL** |
| 630 | Ost-/West-Verschattung | 4 | 2 | 2 | 0 | **FAIL** |
| 640 | Nachtabsenkung | 4 | 4 | 0 | 0 | PASS |
| 650 | Nachtlüftung | 4 | 4 | 0 | 0 | PASS |
| 650FF | Free-Float Nachtlüftung | 3 | 2 | 1 | 0 | **FAIL** |
| 660 | Low-E Verglasung | 4 | 2 | 2 | 0 | **FAIL** |
| 670 | Einscheibenverglasung | 4 | 0 | 4 | 0 | **FAIL** |
| 680 | Erhöhte Dämmung | 4 | 4 | 0 | 0 | PASS |
| 680FF | Free-Float erhöhte Dämmung | 3 | 3 | 0 | 0 | PASS |
| 685 | Thermostat 20/20 | 4 | 3 | 1 | 0 | **FAIL** |
| 695 | Erhöhte Dämmung + 20/20 | 4 | 4 | 0 | 0 | PASS |
| 900 | Schwerbau Basisfall | 28 | 26 | 2 | 0 | **FAIL** |
| 900FF | Free-Float Schwerbau | 3 | 3 | 0 | 0 | PASS |
| 910 | Schwerbau + Süd-Verschattung | 4 | 4 | 0 | 0 | PASS |
| 920 | Schwerbau + Ost-/West-Fenster | 4 | 4 | 0 | 0 | PASS |
| 930 | Schwerbau + Ost-/West-Verschattung | 4 | 3 | 1 | 0 | **FAIL** |
| 940 | Schwerbau + Nachtabsenkung | 4 | 3 | 1 | 0 | **FAIL** |
| 950 | Schwerbau + Nachtlüftung | 4 | 4 | 0 | 0 | PASS |
| 950FF | Free-Float Schwerbau + Nachtlüftung | 3 | 2 | 1 | 0 | **FAIL** |
| 960 | Wintergarten (Sunspace) | 4 | 1 | 3 | 0 | **FAIL** |
| 980 | Schwerbau + erhöhte Dämmung | 4 | 4 | 0 | 0 | PASS |
| 980FF | Free-Float Schwerbau + Dämmung | 3 | 3 | 0 | 0 | PASS |
| 985 | Schwerbau + 20/20 | 4 | 4 | 0 | 0 | PASS |
| 995 | Schwerbau + Dämmung + 20/20 | 4 | 4 | 0 | 0 | PASS |

## Details

### Case 600 — Leichtbau Basisfall **FAIL**
_Leichtbau, Südfenster 12 m², Thermostat 20/27 °C, 0.5 ach, 200 W int. Lasten_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Heizenergie Jan [kWh] | 676.05 | 835.44 | 734.94 | 655.6 | 734.9 | PASS |
| Heizenergie Feb [kWh] | 655.92 | 741.47 | 702.08 | 626.3 | 702.1 | PASS |
| Heizenergie Mar [kWh] | 458.71 | 329.1 | 495.0 | 433.5 | 495.0 | PASS |
| Heizenergie Apr [kWh] | 499.27 | 340.4 | 517.29 | 448.0 | 517.3 | PASS |
| Heizenergie May [kWh] | 132.05 | 32.67 | 150.73 | 112.8 | 150.7 | PASS |
| Heizenergie Jun [kWh] | 7.68 | 0.0 | 15.95 | 2.7 | 16.0 | PASS |
| Heizenergie Jul [kWh] | 9.3 | 0.0 | 16.73 | 4.8 | 16.7 | PASS |
| Heizenergie Aug [kWh] | 5.14 | 0.0 | 9.6 | 1.4 | 9.8 | PASS |
| Heizenergie Sep [kWh] | 69.97 | 2.16 | 84.82 | 51.8 | 89.1 | PASS |
| Heizenergie Oct [kWh] | 337.41 | 195.35 | 367.05 | 317.0 | 370.1 | PASS |
| Heizenergie Nov [kWh] | 598.96 | 679.05 | 645.81 | 575.6 | 647.9 | PASS |
| Heizenergie Dec [kWh] | 693.73 | 830.44 | 754.28 | 682.0 | 763.5 | PASS |
| Kühlenergie Jan [kWh] | 529.34 | 0.0 | 495.01 | 417.9 | 580.9 | PASS |
| Kühlenergie Feb [kWh] | 396.22 | 0.0 | 367.4 | 315.4 | 450.4 | PASS |
| Kühlenergie Mar [kWh] | 490.84 | 0.0 | 457.38 | 410.7 | 594.4 | PASS |
| Kühlenergie Apr [kWh] | 237.77 | 0.74 | 235.36 | 218.7 | 343.7 | PASS |
| Kühlenergie May [kWh] | 309.12 | 143.29 | 325.15 | 321.2 | 461.1 | **FAIL** |
| Kühlenergie Jun [kWh] | 498.9 | 545.28 | 516.06 | 497.4 | 636.0 | PASS |
| Kühlenergie Jul [kWh] | 488.76 | 509.98 | 514.39 | 505.9 | 635.0 | **FAIL** |
| Kühlenergie Aug [kWh] | 617.19 | 460.48 | 634.14 | 606.5 | 739.8 | PASS |
| Kühlenergie Sep [kWh] | 717.91 | 247.22 | 710.47 | 672.1 | 796.7 | PASS |
| Kühlenergie Oct [kWh] | 675.61 | 12.13 | 649.48 | 611.1 | 729.5 | PASS |
| Kühlenergie Nov [kWh] | 452.5 | 0.0 | 418.57 | 377.1 | 480.9 | PASS |
| Kühlenergie Dec [kWh] | 492.85 | 0.0 | 456.1 | 386.2 | 527.7 | PASS |
| Jährliche Heizenergie [MWh] | 4.1442 | 3.9861 | 4.4943 | 3.992755 | 4.50355 | PASS |
| Jährliche Kühlenergie [MWh] | 5.907 | 1.9191 | 5.7795 | 5.432 | 6.976214 | PASS |
| Spitzenheizlast [kW] | 2.9415 | 2.7849 | 3.3589 | 3.020233 | 3.358893 | **FAIL** |
| Spitzenkühllast [kW] | 6.0889 | 2.7815 | 6.0457 | 5.422 | 6.8352 | PASS |

### Case 600FF — Free-Float Leichtbau PASS
_Wie 600, keine Heizung/Kühlung — freie Temperaturentwicklung_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Max. Lufttemperatur [°C] | 64.72 | 27.0 | 62.37 | 62.369162 | 68.36078 | PASS |
| Min. Lufttemperatur [°C] | -11.44 | 20.0 | -13.84 | -13.844209 | -9.9 | PASS |
| Mittl. Lufttemperatur [°C] | 25.64 | 22.88 | 24.27 | 24.2578 | 26.658725 | PASS |

### Case 610 — Süd-Verschattung **FAIL**
_Wie 600 + horizontaler Überhang 1.0 m, 0.5 m über Fensteroberkante_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 4.2688 | 3.9861 | 4.5828 | 4.066423 | 4.59206 | PASS |
| Jährliche Kühlenergie [MWh] | 4.1903 | 1.9191 | 4.1168 | 4.1168 | 4.854538 | PASS |
| Spitzenheizlast [kW] | 2.9412 | 2.7849 | 3.3595 | 3.020759 | 3.359502 | **FAIL** |
| Spitzenkühllast [kW] | 5.7441 | 2.7815 | 5.8678 | 5.331 | 6.4896 | PASS |

### Case 620 — Ost-/West-Fenster **FAIL**
_Wie 600, aber 6 m² Ost + 6 m² West statt 12 m² Süd_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 4.3327 | 3.9861 | 4.7094 | 4.093598 | 4.71898 | PASS |
| Jährliche Kühlenergie [MWh] | 4.1221 | 1.9191 | 3.8407 | 3.84065 | 4.817314 | PASS |
| Spitzenheizlast [kW] | 2.9435 | 2.7849 | 3.3846 | 3.03786 | 3.384592 | **FAIL** |
| Spitzenkühllast [kW] | 4.4486 | 2.7815 | 4.5883 | 3.955 | 4.9008 | PASS |

### Case 630 — Ost-/West-Verschattung **FAIL**
_Wie 620 + Überhang und vertikale Lamellen an Ost-/West-Fenstern_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 4.6265 | 3.9861 | 5.129 | 4.355946 | 5.13858 | PASS |
| Jährliche Kühlenergie [MWh] | 3.1357 | 1.9191 | 2.5729 | 2.57287 | 3.074 | **FAIL** |
| Spitzenheizlast [kW] | 2.9434 | 2.7849 | 3.3876 | 3.039372 | 3.387554 | **FAIL** |
| Spitzenkühllast [kW] | 3.9095 | 2.7815 | 3.9494 | 3.526 | 4.212174 | PASS |

### Case 640 — Nachtabsenkung PASS
_Wie 600 + Heizung Nachtabsenkung auf 10 °C (23:00–07:00)_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 2.5413 | 3.9861 | 2.6452 | 2.403242 | 2.682 | PASS |
| Jährliche Kühlenergie [MWh] | 5.6527 | 1.9191 | 5.4772 | 5.237 | 5.8926 | PASS |
| Spitzenheizlast [kW] | 4.0709 | 2.7849 | 4.0385 | 4.038541 | 4.658 | PASS |
| Spitzenkühllast [kW] | 6.0006 | 2.7815 | 5.9671 | 5.365 | 6.428988 | PASS |

### Case 650 — Nachtlüftung PASS
_Wie 600, keine Heizung, mechanische Lüftung 1700 m³/h (18:00–07:00)_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 0.0 | 3.9861 | 0.0 | 0.0 | 0.0 | PASS |
| Jährliche Kühlenergie [MWh] | 4.5592 | 1.9191 | 4.6323 | 4.186 | 5.545075 | PASS |
| Spitzenheizlast [kW] | 0.0 | 2.7849 | 0.0 | 0.0 | 0.0 | PASS |
| Spitzenkühllast [kW] | 5.6831 | 2.7815 | 5.7975 | 5.045 | 6.5712 | PASS |

### Case 650FF — Free-Float Nachtlüftung **FAIL**
_Wie 650 (Nachtlüftung) ohne HVAC, freie Temperaturen_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Max. Lufttemperatur [°C] | 62.53 | 27.0 | 61.13 | 61.133168 | 66.84649 | PASS |
| Min. Lufttemperatur [°C] | -15.29 | 20.0 | -17.49 | -17.76156 | -15.81 | **FAIL** |
| Mittl. Lufttemperatur [°C] | 18.33 | 22.88 | 18.41 | 17.6 | 19.798065 | PASS |

### Case 660 — Low-E Verglasung **FAIL**
_Wie 600, Low-E Argon-Verglasung statt Zweischeiben-Klarverglasung_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 3.4028 | 3.9861 | 3.7816 | 3.574 | 3.91681 | **FAIL** |
| Jährliche Kühlenergie [MWh] | 3.334 | 1.9191 | 2.9663 | 2.96625 | 3.641256 | PASS |
| Spitzenheizlast [kW] | 2.4201 | 2.7849 | 2.9552 | 2.62 | 2.955183 | **FAIL** |
| Spitzenkühllast [kW] | 3.6202 | 2.7815 | 3.4574 | 3.343 | 3.933001 | PASS |

### Case 670 — Einscheibenverglasung **FAIL**
_Wie 600, Einscheiben-Klarverglasung statt Zweischeiben_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 3.977 | 3.9861 | 6.1281 | 5.300178 | 7.109126 | **FAIL** |
| Jährliche Kühlenergie [MWh] | 8.1544 | 1.9191 | 6.1978 | 5.954 | 6.622703 | **FAIL** |
| Spitzenheizlast [kW] | 2.9489 | 2.7849 | 4.221 | 3.655419 | 4.488 | **FAIL** |
| Spitzenkühllast [kW] | 7.568 | 2.7815 | 6.4013 | 5.839 | 6.925312 | **FAIL** |

### Case 680 — Erhöhte Dämmung PASS
_Wie 600, Wand 0.250 m und Dach 0.400 m Dämmung (statt 0.066/0.112 m)_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 2.0197 | 3.9861 | 2.2809 | 1.732 | 2.28626 | PASS |
| Jährliche Kühlenergie [MWh] | 6.5383 | 1.9191 | 6.3097 | 5.932 | 7.652995 | PASS |
| Spitzenheizlast [kW] | 1.9308 | 2.7849 | 2.1147 | 1.777641 | 2.126 | PASS |
| Spitzenkühllast [kW] | 6.4805 | 2.7815 | 6.5566 | 5.761 | 7.2912 | PASS |

### Case 680FF — Free-Float erhöhte Dämmung PASS
_Wie 680 (erhöhte Dämmung) ohne HVAC, freie Temperaturen_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Max. Lufttemperatur [°C] | 73.35 | 27.0 | 69.77 | 69.774156 | 81.48 | PASS |
| Min. Lufttemperatur [°C] | -6.28 | 20.0 | -8.07 | -8.073551 | -5.7 | PASS |
| Mittl. Lufttemperatur [°C] | 32.68 | 22.88 | 30.19 | 30.1869 | 36.364849 | PASS |

### Case 685 — Thermostat 20/20 **FAIL**
_Wie 600, Thermostat 20/20 °C (kein Totband)_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 4.766 | 3.9861 | 5.0327 | 4.532 | 5.059291 | PASS |
| Jährliche Kühlenergie [MWh] | 8.9849 | 1.9191 | 8.8513 | 8.238 | 9.919776 | PASS |
| Spitzenheizlast [kW] | 2.9418 | 2.7849 | 3.3744 | 3.031857 | 3.374427 | **FAIL** |
| Spitzenkühllast [kW] | 6.7976 | 2.7815 | 6.8674 | 6.071 | 7.4592 | PASS |

### Case 695 — Erhöhte Dämmung + 20/20 PASS
_Kombination aus Case 680 (Dämmung) + Case 685 (Thermostat)_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 2.7036 | 3.9861 | 2.8859 | 2.385 | 2.89174 | PASS |
| Jährliche Kühlenergie [MWh] | 9.2627 | 1.9191 | 9.0391 | 8.386 | 10.126306 | PASS |
| Spitzenheizlast [kW] | 1.9333 | 2.7849 | 2.1177 | 1.795326 | 2.138 | PASS |
| Spitzenkühllast [kW] | 7.0325 | 2.7815 | 7.1752 | 6.232 | 7.7232 | PASS |

### Case 900 — Schwerbau Basisfall **FAIL**
_Wie 600, aber Betonstein-Wände und Bodenplatte statt Leichtbau_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Heizenergie Jan [kWh] | 247.09 | 835.44 | 291.94 | 206.1 | 291.9 | PASS |
| Heizenergie Feb [kWh] | 292.23 | 741.47 | 322.14 | 243.2 | 322.1 | PASS |
| Heizenergie Mar [kWh] | 131.8 | 329.1 | 143.84 | 102.4 | 143.8 | PASS |
| Heizenergie Apr [kWh] | 274.17 | 340.4 | 275.47 | 214.2 | 275.7 | PASS |
| Heizenergie May [kWh] | 36.8 | 32.67 | 37.5 | 20.1 | 37.5 | PASS |
| Heizenergie Jun [kWh] | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | PASS |
| Heizenergie Jul [kWh] | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | PASS |
| Heizenergie Aug [kWh] | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | PASS |
| Heizenergie Sep [kWh] | 0.04 | 2.16 | 0.54 | 0.0 | 2.1 | PASS |
| Heizenergie Oct [kWh] | 83.67 | 195.35 | 85.01 | 63.6 | 85.0 | PASS |
| Heizenergie Nov [kWh] | 287.06 | 679.05 | 318.24 | 251.6 | 318.2 | PASS |
| Heizenergie Dec [kWh] | 294.52 | 830.44 | 333.38 | 254.7 | 339.4 | PASS |
| Kühlenergie Jan [kWh] | 93.13 | 0.0 | 44.63 | 33.5 | 100.1 | PASS |
| Kühlenergie Feb [kWh] | 40.37 | 0.0 | 9.24 | 4.7 | 42.5 | PASS |
| Kühlenergie Mar [kWh] | 110.89 | 0.0 | 50.55 | 40.9 | 144.1 | PASS |
| Kühlenergie Apr [kWh] | 36.03 | 0.74 | 16.05 | 12.3 | 71.2 | PASS |
| Kühlenergie May [kWh] | 123.2 | 143.29 | 98.35 | 98.4 | 210.7 | PASS |
| Kühlenergie Jun [kWh] | 395.33 | 545.28 | 365.82 | 365.8 | 512.9 | PASS |
| Kühlenergie Jul [kWh] | 385.87 | 509.98 | 365.51 | 365.5 | 510.7 | PASS |
| Kühlenergie Aug [kWh] | 514.24 | 460.48 | 487.57 | 485.7 | 620.9 | PASS |
| Kühlenergie Sep [kWh] | 524.25 | 247.22 | 458.86 | 458.9 | 573.9 | PASS |
| Kühlenergie Oct [kWh] | 343.85 | 12.13 | 260.85 | 260.9 | 358.6 | PASS |
| Kühlenergie Nov [kWh] | 106.88 | 0.0 | 60.18 | 56.2 | 104.1 | **FAIL** |
| Kühlenergie Dec [kWh] | 102.31 | 0.0 | 49.5 | 38.1 | 95.9 | **FAIL** |
| Jährliche Heizenergie [MWh] | 1.6474 | 3.9861 | 1.8081 | 1.378891 | 1.81403 | PASS |
| Jährliche Kühlenergie [MWh] | 2.7763 | 1.9191 | 2.2671 | 2.26713 | 3.345562 | PASS |
| Spitzenheizlast [kW] | 2.5798 | 2.7849 | 2.7785 | 2.44339 | 2.778478 | PASS |
| Spitzenkühllast [kW] | 3.1745 | 2.7815 | 2.9401 | 2.556 | 3.768 | PASS |

### Case 900FF — Free-Float Schwerbau PASS
_Wie 900 (Schwerbau) ohne HVAC, freie Temperaturen_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Max. Lufttemperatur [°C] | 45.5 | 27.0 | 43.25 | 43.252232 | 46.17 | PASS |
| Min. Lufttemperatur [°C] | 1.81 | 20.0 | 0.64 | 0.6 | 2.49 | PASS |
| Mittl. Lufttemperatur [°C] | 25.7 | 22.88 | 24.47 | 24.4623 | 26.72271 | PASS |

### Case 910 — Schwerbau + Süd-Verschattung PASS
_Kombination Case 900 (Schwerbau) + Case 610 (Überhang)_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 2.012 | 3.9861 | 2.1258 | 1.647682 | 2.163 | PASS |
| Jährliche Kühlenergie [MWh] | 1.5528 | 1.9191 | 1.1909 | 1.19086 | 1.748174 | PASS |
| Spitzenheizlast [kW] | 2.6007 | 2.7849 | 2.7992 | 2.469025 | 2.799195 | PASS |
| Spitzenkühllast [kW] | 2.5119 | 2.7815 | 2.081 | 2.081035 | 2.7648 | PASS |

### Case 920 — Schwerbau + Ost-/West-Fenster PASS
_Kombination Case 900 + Case 620 (Ost-/West-Fenster)_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 3.2941 | 3.9861 | 3.5991 | 2.956069 | 3.6067 | PASS |
| Jährliche Kühlenergie [MWh] | 2.9638 | 1.9191 | 2.5489 | 2.54887 | 3.257059 | PASS |
| Spitzenheizlast [kW] | 2.6565 | 2.7849 | 2.8643 | 2.512426 | 2.895 | PASS |
| Spitzenkühllast [kW] | 3.2962 | 2.7815 | 3.1541 | 2.71 | 3.672 | PASS |

### Case 930 — Schwerbau + Ost-/West-Verschattung **FAIL**
_Kombination Case 900 + Case 630 (Ost-/West-Verschattung)_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 3.848 | 3.9861 | 4.3762 | 3.523647 | 4.3841 | PASS |
| Jährliche Kühlenergie [MWh] | 2.2637 | 1.9191 | 1.6718 | 1.6538 | 2.161 | **FAIL** |
| Spitzenheizlast [kW] | 2.6726 | 2.7849 | 2.9004 | 2.536968 | 2.968 | PASS |
| Spitzenkühllast [kW] | 2.8387 | 2.7815 | 2.6131 | 2.335 | 3.052 | PASS |

### Case 940 — Schwerbau + Nachtabsenkung **FAIL**
_Kombination Case 900 + Case 640 (Nachtabsenkung)_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 1.0592 | 3.9861 | 1.1642 | 0.863236 | 1.389 | PASS |
| Jährliche Kühlenergie [MWh] | 2.6692 | 1.9191 | 2.2035 | 2.20346 | 2.613 | **FAIL** |
| Spitzenheizlast [kW] | 3.301 | 2.7849 | 3.4048 | 3.051914 | 3.882 | PASS |
| Spitzenkühllast [kW] | 3.1751 | 2.7815 | 2.9376 | 2.556 | 3.376435 | PASS |

### Case 950 — Schwerbau + Nachtlüftung PASS
_Kombination Case 900 + Case 650 (Nachtlüftung); Masse speichert Nachtkühle_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 0.0 | 3.9861 | 0.0 | 0.0 | 0.0 | PASS |
| Jährliche Kühlenergie [MWh] | 0.809 | 1.9191 | 0.6416 | 0.586 | 0.90048 | PASS |
| Spitzenheizlast [kW] | 0.0 | 2.7849 | 0.0 | 0.0 | 0.0 | PASS |
| Spitzenkühllast [kW] | 2.5606 | 2.7815 | 2.2364 | 2.054 | 2.928 | PASS |

### Case 950FF — Free-Float Schwerbau + Nachtlüftung **FAIL**
_Wie 950 (Schwerbau + Nachtlüftung) ohne HVAC, freie Temperaturen_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Max. Lufttemperatur [°C] | 37.77 | 27.0 | 36.13 | 36.126665 | 37.1 | **FAIL** |
| Min. Lufttemperatur [°C] | -12.53 | 20.0 | -12.8 | -13.36 | -11.14 | PASS |
| Mittl. Lufttemperatur [°C] | 14.97 | 22.88 | 14.69 | 14.35 | 15.522804 | PASS |

### Case 960 — Wintergarten (Sunspace) **FAIL**
_Zwei-Zonen-Gebäude: Hinterzone (Leichtbau), Wintergarten (Schwerbau, 2 m tief)_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 2.7442 | 3.9861 | 2.8535 | 2.522072 | 2.85954 | PASS |
| Jährliche Kühlenergie [MWh] | 0.6735 | 1.9191 | 0.789 | 0.788958 | 0.955762 | **FAIL** |
| Spitzenheizlast [kW] | 1.8797 | 2.7849 | 2.3004 | 2.085 | 2.300402 | **FAIL** |
| Spitzenkühllast [kW] | 1.2715 | 2.7815 | 1.3385 | 1.338487 | 1.479919 | **FAIL** |

### Case 980 — Schwerbau + erhöhte Dämmung PASS
_Kombination Case 900 + Case 680 (erhöhte Dämmung)_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 0.4006 | 3.9861 | 0.4474 | 0.245766 | 0.72 | PASS |
| Jährliche Kühlenergie [MWh] | 4.1923 | 1.9191 | 3.5185 | 3.501 | 5.207938 | PASS |
| Spitzenheizlast [kW] | 1.5982 | 2.7849 | 1.5921 | 1.25379 | 1.693 | PASS |
| Spitzenkühllast [kW] | 3.6355 | 2.7815 | 3.3126 | 2.93 | 4.2288 | PASS |

### Case 980FF — Free-Float Schwerbau + Dämmung PASS
_Wie 980 (Schwerbau + Dämmung) ohne HVAC, höchste Sommertemperaturen_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Max. Lufttemperatur [°C] | 53.45 | 27.0 | 48.54 | 48.540639 | 55.95 | PASS |
| Min. Lufttemperatur [°C] | 11.69 | 20.0 | 9.47 | 7.3 | 13.11 | PASS |
| Mittl. Lufttemperatur [°C] | 32.66 | 22.88 | 30.5 | 30.492 | 36.362946 | PASS |

### Case 985 — Schwerbau + 20/20 PASS
_Kombination Case 900 + Case 685 (Thermostat 20/20)_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 2.5728 | 3.9861 | 2.5304 | 2.12021 | 2.870693 | PASS |
| Jährliche Kühlenergie [MWh] | 6.8015 | 1.9191 | 6.1135 | 5.88 | 7.75909 | PASS |
| Spitzenheizlast [kW] | 2.5906 | 2.7849 | 2.7854 | 2.452163 | 2.785441 | PASS |
| Spitzenkühllast [kW] | 3.9748 | 2.7815 | 3.8847 | 3.208 | 4.5312 | PASS |

### Case 995 — Schwerbau + Dämmung + 20/20 PASS
_Kombination Case 900 + Case 695 (erhöhte Dämmung + Thermostat 20/20)_

| Metrik | NANDRAD | EnergyPlus | TRNSYS | Ref Min | Ref Max | Status |
|--------|---------|------------|--------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 1.0984 | 3.9861 | 1.0737 | 0.755182 | 1.33 | PASS |
| Jährliche Kühlenergie [MWh] | 7.6482 | 1.9191 | 7.0638 | 6.771 | 8.610787 | PASS |
| Spitzenheizlast [kW] | 1.6664 | 2.7849 | 1.662 | 1.369555 | 1.711 | PASS |
| Spitzenkühllast [kW] | 4.1788 | 2.7815 | 4.1149 | 3.315 | 4.9248 | PASS |
