# Case 980: High-Mass Increased Exterior Wall and Roof Insulation

## Base Case

Based on Case 900, with increased insulation in exterior walls and roof.

## Changes from Case 900

- Exterior wall foam insulation thickness increased from 0.0615 m to 0.2452 m.
- Roof fiberglass quilt thickness increased from 0.1118 m to 0.4 m.
- Floor is unchanged from Case 900.

## Construction -- Exterior Wall (inside to outside)

| Layer | k [W/(m-K)] | Thickness [m] | U [W/(m^2-K)] | R [m^2-K/W] | Density [kg/m^3] | cp [J/(kg-K)] |
|-------|-------------|---------------|----------------|-------------|-------------------|---------------|
| Concrete Block | 0.51 | 0.100 | 5.100 | 0.196 | 1400 | 1000 |
| **Foam Insulation** | **0.04** | **0.2452** | **0.163** | **6.130** | **10** | **1400** |
| Wood Siding | 0.14 | 0.009 | 15.556 | 0.064 | 530 | 900 |

Summary: Total air-to-air U = 0.143 W/(m^2-K), R = 6.992 m^2-K/W, Wall UA = 9.096 W/K.

## Construction -- Roof (inside to outside)

| Layer | k [W/(m-K)] | Thickness [m] | U [W/(m^2-K)] | R [m^2-K/W] | Density [kg/m^3] | cp [J/(kg-K)] |
|-------|-------------|---------------|----------------|-------------|-------------------|---------------|
| Plasterboard | 0.16 | 0.010 | 16.000 | 0.063 | 950 | 840 |
| **Fiberglass quilt** | **0.04** | **0.4** | **0.100** | **10.000** | **12** | **840** |
| Roofdeck | 0.14 | 0.019 | 7.368 | 0.136 | 530 | 900 |

Summary: Total air-to-air U = 0.092 W/(m^2-K), R = 10.832 m^2-K/W, Roof UA = 4.431 W/K. The Case 980 roof is the same as the low-mass Case 680 roof.

## Summary (Case 980 vs. Case 900)

| Component | Area [m^2] | UA [W/K] |
|-----------|-----------|----------|
| Wall | 63.6 | 9.096 |
| Floor | 48.0 | 1.867 |
| Roof | 48.0 | 4.431 |
| S. Window | 12.0 | 25.184 |
| Infiltration | -- | 18.555 |
| **Total** | -- | **59.133** |

Internal heat capacity: 15075 kJ/K. Total heat capacity: 15783 kJ/K.

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- Additional output specified for Case 980 in Section 6.2.1.8
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- This is the high-mass equivalent of Case 680 -- increased insulation with massive wall and floor construction.
- The floor construction is unchanged from Case 900.
- Wall insulation thickness differs slightly from Case 680 (0.2452 m vs. 0.250 m) to better match total floor R-values between low-mass and high-mass cases.
