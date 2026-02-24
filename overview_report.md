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

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Heizenergie Jan [kWh] | 670.57 | 655.6 | 734.9 | PASS |
| Heizenergie Feb [kWh] | 650.51 | 626.3 | 702.1 | PASS |
| Heizenergie Mar [kWh] | 454.68 | 433.5 | 495.0 | PASS |
| Heizenergie Apr [kWh] | 494.86 | 448.0 | 517.3 | PASS |
| Heizenergie May [kWh] | 130.47 | 112.8 | 150.7 | PASS |
| Heizenergie Jun [kWh] | 7.45 | 2.7 | 16.0 | PASS |
| Heizenergie Jul [kWh] | 9.09 | 4.8 | 16.7 | PASS |
| Heizenergie Aug [kWh] | 5.0 | 1.4 | 9.8 | PASS |
| Heizenergie Sep [kWh] | 69.02 | 51.8 | 89.1 | PASS |
| Heizenergie Oct [kWh] | 334.26 | 317.0 | 370.1 | PASS |
| Heizenergie Nov [kWh] | 594.13 | 575.6 | 647.9 | PASS |
| Heizenergie Dec [kWh] | 688.17 | 682.0 | 763.5 | PASS |
| Kühlenergie Jan [kWh] | 531.51 | 417.9 | 580.9 | PASS |
| Kühlenergie Feb [kWh] | 398.07 | 315.4 | 450.4 | PASS |
| Kühlenergie Mar [kWh] | 492.44 | 410.7 | 594.4 | PASS |
| Kühlenergie Apr [kWh] | 238.74 | 218.7 | 343.7 | PASS |
| Kühlenergie May [kWh] | 309.91 | 321.2 | 461.1 | **FAIL** |
| Kühlenergie Jun [kWh] | 498.93 | 497.4 | 636.0 | PASS |
| Kühlenergie Jul [kWh] | 488.99 | 505.9 | 635.0 | **FAIL** |
| Kühlenergie Aug [kWh] | 617.31 | 606.5 | 739.8 | PASS |
| Kühlenergie Sep [kWh] | 718.43 | 672.1 | 796.7 | PASS |
| Kühlenergie Oct [kWh] | 676.87 | 611.1 | 729.5 | PASS |
| Kühlenergie Nov [kWh] | 454.2 | 377.1 | 480.9 | PASS |
| Kühlenergie Dec [kWh] | 494.84 | 386.2 | 527.7 | PASS |
| Jährliche Heizenergie [MWh] | 4.1082 | 3.992755 | 4.50355 | PASS |
| Jährliche Kühlenergie [MWh] | 5.9203 | 5.432 | 6.976214 | PASS |
| Spitzenheizlast [kW] | 2.9236 | 3.020233 | 3.358893 | **FAIL** |
| Spitzenkühllast [kW] | 6.0939 | 5.422 | 6.8352 | PASS |

### Case 600FF — Free-Float Leichtbau PASS
_Wie 600, keine Heizung/Kühlung — freie Temperaturentwicklung_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Max. Lufttemperatur [°C] | 64.87 | 62.369162 | 68.36078 | PASS |
| Min. Lufttemperatur [°C] | -11.4 | -13.844209 | -9.9 | PASS |
| Mittl. Lufttemperatur [°C] | 25.72 | 24.2578 | 26.658725 | PASS |

### Case 610 — Süd-Verschattung **FAIL**
_Wie 600 + horizontaler Überhang 1.0 m, 0.5 m über Fensteroberkante_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 4.232 | 4.066423 | 4.59206 | PASS |
| Jährliche Kühlenergie [MWh] | 4.2021 | 4.1168 | 4.854538 | PASS |
| Spitzenheizlast [kW] | 2.9231 | 3.020759 | 3.359502 | **FAIL** |
| Spitzenkühllast [kW] | 5.7493 | 5.331 | 6.4896 | PASS |

### Case 620 — Ost-/West-Fenster **FAIL**
_Wie 600, aber 6 m² Ost + 6 m² West statt 12 m² Süd_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 4.2945 | 4.093598 | 4.71898 | PASS |
| Jährliche Kühlenergie [MWh] | 4.1311 | 3.84065 | 4.817314 | PASS |
| Spitzenheizlast [kW] | 2.9253 | 3.03786 | 3.384592 | **FAIL** |
| Spitzenkühllast [kW] | 4.4419 | 3.955 | 4.9008 | PASS |

### Case 630 — Ost-/West-Verschattung **FAIL**
_Wie 620 + Überhang und vertikale Lamellen an Ost-/West-Fenstern_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 4.5861 | 4.355946 | 5.13858 | PASS |
| Jährliche Kühlenergie [MWh] | 3.1418 | 2.57287 | 3.074 | **FAIL** |
| Spitzenheizlast [kW] | 2.9254 | 3.039372 | 3.387554 | **FAIL** |
| Spitzenkühllast [kW] | 3.901 | 3.526 | 4.212174 | PASS |

### Case 640 — Nachtabsenkung PASS
_Wie 600 + Heizung Nachtabsenkung auf 10 °C (23:00–07:00)_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 2.5171 | 2.403242 | 2.682 | PASS |
| Jährliche Kühlenergie [MWh] | 5.6654 | 5.237 | 5.8926 | PASS |
| Spitzenheizlast [kW] | 4.059 | 4.038541 | 4.658 | PASS |
| Spitzenkühllast [kW] | 6.0071 | 5.365 | 6.428988 | PASS |

### Case 650 — Nachtlüftung PASS
_Wie 600, keine Heizung, mechanische Lüftung 1700 m³/h (18:00–07:00)_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 0.0 | 0.0 | 0.0 | PASS |
| Jährliche Kühlenergie [MWh] | 4.5689 | 4.186 | 5.545075 | PASS |
| Spitzenheizlast [kW] | 0.0 | 0.0 | 0.0 | PASS |
| Spitzenkühllast [kW] | 5.6811 | 5.045 | 6.5712 | PASS |

### Case 650FF — Free-Float Nachtlüftung **FAIL**
_Wie 650 (Nachtlüftung) ohne HVAC, freie Temperaturen_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Max. Lufttemperatur [°C] | 62.64 | 61.133168 | 66.84649 | PASS |
| Min. Lufttemperatur [°C] | -15.28 | -17.76156 | -15.81 | **FAIL** |
| Mittl. Lufttemperatur [°C] | 18.38 | 17.6 | 19.798065 | PASS |

### Case 660 — Low-E Verglasung **FAIL**
_Wie 600, Low-E Argon-Verglasung statt Zweischeiben-Klarverglasung_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 3.3661 | 3.574 | 3.91681 | **FAIL** |
| Jährliche Kühlenergie [MWh] | 3.3453 | 2.96625 | 3.641256 | PASS |
| Spitzenheizlast [kW] | 2.4023 | 2.62 | 2.955183 | **FAIL** |
| Spitzenkühllast [kW] | 3.6229 | 3.343 | 3.933001 | PASS |

### Case 670 — Einscheibenverglasung **FAIL**
_Wie 600, Einscheiben-Klarverglasung statt Zweischeiben_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 3.9421 | 5.300178 | 7.109126 | **FAIL** |
| Jährliche Kühlenergie [MWh] | 8.1689 | 5.954 | 6.622703 | **FAIL** |
| Spitzenheizlast [kW] | 2.9306 | 3.655419 | 4.488 | **FAIL** |
| Spitzenkühllast [kW] | 7.5746 | 5.839 | 6.925312 | **FAIL** |

### Case 680 — Erhöhte Dämmung PASS
_Wie 600, Wand 0.250 m und Dach 0.400 m Dämmung (statt 0.066/0.112 m)_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 1.9876 | 1.732 | 2.28626 | PASS |
| Jährliche Kühlenergie [MWh] | 6.5568 | 5.932 | 7.652995 | PASS |
| Spitzenheizlast [kW] | 1.9128 | 1.777641 | 2.126 | PASS |
| Spitzenkühllast [kW] | 6.4858 | 5.761 | 7.2912 | PASS |

### Case 680FF — Free-Float erhöhte Dämmung PASS
_Wie 680 (erhöhte Dämmung) ohne HVAC, freie Temperaturen_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Max. Lufttemperatur [°C] | 73.69 | 69.774156 | 81.48 | PASS |
| Min. Lufttemperatur [°C] | -6.17 | -8.073551 | -5.7 | PASS |
| Mittl. Lufttemperatur [°C] | 32.86 | 30.1869 | 36.364849 | PASS |

### Case 685 — Thermostat 20/20 **FAIL**
_Wie 600, Thermostat 20/20 °C (kein Totband)_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 4.73 | 4.532 | 5.059291 | PASS |
| Jährliche Kühlenergie [MWh] | 8.9891 | 8.238 | 9.919776 | PASS |
| Spitzenheizlast [kW] | 2.9234 | 3.031857 | 3.374427 | **FAIL** |
| Spitzenkühllast [kW] | 6.8004 | 6.071 | 7.4592 | PASS |

### Case 695 — Erhöhte Dämmung + 20/20 PASS
_Kombination aus Case 680 (Dämmung) + Case 685 (Thermostat)_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 2.6702 | 2.385 | 2.89174 | PASS |
| Jährliche Kühlenergie [MWh] | 9.2693 | 8.386 | 10.126306 | PASS |
| Spitzenheizlast [kW] | 1.9152 | 1.795326 | 2.138 | PASS |
| Spitzenkühllast [kW] | 7.0372 | 6.232 | 7.7232 | PASS |

### Case 900 — Schwerbau Basisfall **FAIL**
_Wie 600, aber Betonstein-Wände und Bodenplatte statt Leichtbau_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Heizenergie Jan [kWh] | 241.97 | 206.1 | 291.9 | PASS |
| Heizenergie Feb [kWh] | 287.06 | 243.2 | 322.1 | PASS |
| Heizenergie Mar [kWh] | 128.74 | 102.4 | 143.8 | PASS |
| Heizenergie Apr [kWh] | 270.23 | 214.2 | 275.7 | PASS |
| Heizenergie May [kWh] | 36.1 | 20.1 | 37.5 | PASS |
| Heizenergie Jun [kWh] | 0.0 | 0.0 | 0.0 | PASS |
| Heizenergie Jul [kWh] | -0.0 | 0.0 | 0.0 | PASS |
| Heizenergie Aug [kWh] | 0.0 | 0.0 | 0.0 | PASS |
| Heizenergie Sep [kWh] | 0.02 | 0.0 | 2.1 | PASS |
| Heizenergie Oct [kWh] | 82.31 | 63.6 | 85.0 | PASS |
| Heizenergie Nov [kWh] | 282.8 | 251.6 | 318.2 | PASS |
| Heizenergie Dec [kWh] | 289.55 | 254.7 | 339.4 | PASS |
| Kühlenergie Jan [kWh] | 94.63 | 33.5 | 100.1 | PASS |
| Kühlenergie Feb [kWh] | 41.37 | 4.7 | 42.5 | PASS |
| Kühlenergie Mar [kWh] | 112.68 | 40.9 | 144.1 | PASS |
| Kühlenergie Apr [kWh] | 36.82 | 12.3 | 71.2 | PASS |
| Kühlenergie May [kWh] | 124.4 | 98.4 | 210.7 | PASS |
| Kühlenergie Jun [kWh] | 396.22 | 365.8 | 512.9 | PASS |
| Kühlenergie Jul [kWh] | 386.85 | 365.5 | 510.7 | PASS |
| Kühlenergie Aug [kWh] | 515.44 | 485.7 | 620.9 | PASS |
| Kühlenergie Sep [kWh] | 525.98 | 458.9 | 573.9 | PASS |
| Kühlenergie Oct [kWh] | 346.47 | 260.9 | 358.6 | PASS |
| Kühlenergie Nov [kWh] | 108.3 | 56.2 | 104.1 | **FAIL** |
| Kühlenergie Dec [kWh] | 103.85 | 38.1 | 95.9 | **FAIL** |
| Jährliche Heizenergie [MWh] | 1.6188 | 1.378891 | 1.81403 | PASS |
| Jährliche Kühlenergie [MWh] | 2.793 | 2.26713 | 3.345562 | PASS |
| Spitzenheizlast [kW] | 2.5618 | 2.44339 | 2.778478 | PASS |
| Spitzenkühllast [kW] | 3.177 | 2.556 | 3.768 | PASS |

### Case 900FF — Free-Float Schwerbau PASS
_Wie 900 (Schwerbau) ohne HVAC, freie Temperaturen_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Max. Lufttemperatur [°C] | 45.59 | 43.252232 | 46.17 | PASS |
| Min. Lufttemperatur [°C] | 1.92 | 0.6 | 2.49 | PASS |
| Mittl. Lufttemperatur [°C] | 25.78 | 24.4623 | 26.72271 | PASS |

### Case 910 — Schwerbau + Süd-Verschattung PASS
_Kombination Case 900 (Schwerbau) + Case 610 (Überhang)_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 1.9798 | 1.647682 | 2.163 | PASS |
| Jährliche Kühlenergie [MWh] | 1.5642 | 1.19086 | 1.748174 | PASS |
| Spitzenheizlast [kW] | 2.5829 | 2.469025 | 2.799195 | PASS |
| Spitzenkühllast [kW] | 2.5176 | 2.081035 | 2.7648 | PASS |

### Case 920 — Schwerbau + Ost-/West-Fenster PASS
_Kombination Case 900 + Case 620 (Ost-/West-Fenster)_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 3.2561 | 2.956069 | 3.6067 | PASS |
| Jährliche Kühlenergie [MWh] | 2.9736 | 2.54887 | 3.257059 | PASS |
| Spitzenheizlast [kW] | 2.6386 | 2.512426 | 2.895 | PASS |
| Spitzenkühllast [kW] | 3.291 | 2.71 | 3.672 | PASS |

### Case 930 — Schwerbau + Ost-/West-Verschattung **FAIL**
_Kombination Case 900 + Case 630 (Ost-/West-Verschattung)_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 3.8081 | 3.523647 | 4.3841 | PASS |
| Jährliche Kühlenergie [MWh] | 2.271 | 1.6538 | 2.161 | **FAIL** |
| Spitzenheizlast [kW] | 2.6551 | 2.536968 | 2.968 | PASS |
| Spitzenkühllast [kW] | 2.8334 | 2.335 | 3.052 | PASS |

### Case 940 — Schwerbau + Nachtabsenkung **FAIL**
_Kombination Case 900 + Case 640 (Nachtabsenkung)_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 1.0398 | 0.863236 | 1.389 | PASS |
| Jährliche Kühlenergie [MWh] | 2.6864 | 2.20346 | 2.613 | **FAIL** |
| Spitzenheizlast [kW] | 3.2816 | 3.051914 | 3.882 | PASS |
| Spitzenkühllast [kW] | 3.1773 | 2.556 | 3.376435 | PASS |

### Case 950 — Schwerbau + Nachtlüftung PASS
_Kombination Case 900 + Case 650 (Nachtlüftung); Masse speichert Nachtkühle_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 0.0 | 0.0 | 0.0 | PASS |
| Jährliche Kühlenergie [MWh] | 0.8158 | 0.586 | 0.90048 | PASS |
| Spitzenheizlast [kW] | 0.0 | 0.0 | 0.0 | PASS |
| Spitzenkühllast [kW] | 2.5655 | 2.054 | 2.928 | PASS |

### Case 950FF — Free-Float Schwerbau + Nachtlüftung **FAIL**
_Wie 950 (Schwerbau + Nachtlüftung) ohne HVAC, freie Temperaturen_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Max. Lufttemperatur [°C] | 37.84 | 36.126665 | 37.1 | **FAIL** |
| Min. Lufttemperatur [°C] | -12.45 | -13.36 | -11.14 | PASS |
| Mittl. Lufttemperatur [°C] | 15.04 | 14.35 | 15.522804 | PASS |

### Case 960 — Wintergarten (Sunspace) **FAIL**
_Zwei-Zonen-Gebäude: Hinterzone (Leichtbau), Wintergarten (Schwerbau, 2 m tief)_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 2.6982 | 2.522072 | 2.85954 | PASS |
| Jährliche Kühlenergie [MWh] | 0.6777 | 0.788958 | 0.955762 | **FAIL** |
| Spitzenheizlast [kW] | 1.8604 | 2.085 | 2.300402 | **FAIL** |
| Spitzenkühllast [kW] | 1.2659 | 1.338487 | 1.479919 | **FAIL** |

### Case 980 — Schwerbau + erhöhte Dämmung PASS
_Kombination Case 900 + Case 680 (erhöhte Dämmung)_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 0.387 | 0.245766 | 0.72 | PASS |
| Jährliche Kühlenergie [MWh] | 4.2289 | 3.501 | 5.207938 | PASS |
| Spitzenheizlast [kW] | 1.5791 | 1.25379 | 1.693 | PASS |
| Spitzenkühllast [kW] | 3.6399 | 2.93 | 4.2288 | PASS |

### Case 980FF — Free-Float Schwerbau + Dämmung PASS
_Wie 980 (Schwerbau + Dämmung) ohne HVAC, höchste Sommertemperaturen_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Max. Lufttemperatur [°C] | 53.72 | 48.540639 | 55.95 | PASS |
| Min. Lufttemperatur [°C] | 11.88 | 7.3 | 13.11 | PASS |
| Mittl. Lufttemperatur [°C] | 32.85 | 30.492 | 36.362946 | PASS |

### Case 985 — Schwerbau + 20/20 PASS
_Kombination Case 900 + Case 685 (Thermostat 20/20)_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 2.5414 | 2.12021 | 2.870693 | PASS |
| Jährliche Kühlenergie [MWh] | 6.81 | 5.88 | 7.75909 | PASS |
| Spitzenheizlast [kW] | 2.5727 | 2.452163 | 2.785441 | PASS |
| Spitzenkühllast [kW] | 3.9736 | 3.208 | 4.5312 | PASS |

### Case 995 — Schwerbau + Dämmung + 20/20 PASS
_Kombination Case 900 + Case 695 (erhöhte Dämmung + Thermostat 20/20)_

| Metrik | NANDRAD | Ref Min | Ref Max | Status |
|--------|---------|---------|---------|--------|
| Jährliche Heizenergie [MWh] | 1.0747 | 0.755182 | 1.33 | PASS |
| Jährliche Kühlenergie [MWh] | 7.6645 | 6.771 | 8.610787 | PASS |
| Spitzenheizlast [kW] | 1.6483 | 1.369555 | 1.711 | PASS |
| Spitzenkühllast [kW] | 4.183 | 3.315 | 4.9248 | PASS |
