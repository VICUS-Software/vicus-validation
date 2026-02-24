# Case 680: Increased Exterior Wall and Roof Insulation

## Base Case

Based on Case 600, with increased insulation in exterior walls and roof.

## Changes from Case 600

- Exterior wall insulation: fiberglass quilt replaced by foam insulation with increased thickness (0.250 m vs. 0.066 m)
- Roof fiberglass quilt thickness increased from 0.1118 m to 0.400 m
- Floor is unchanged from Case 600

## Construction -- Exterior Wall (inside to outside)

| Layer | k [W/(m-K)] | Thickness [m] | U [W/(m^2-K)] | R [m^2-K/W] | Density [kg/m^3] | cp [J/(kg-K)] |
|-------|-------------|---------------|----------------|-------------|-------------------|---------------|
| Plasterboard | 0.16 | 0.012 | 13.333 | 0.075 | 950 | 840 |
| **Foam Insulation** | **0.04** | **0.250** | -- | **6.250** | **10** | **1400** |
| Wood Siding | 0.14 | 0.009 | 15.556 | 0.064 | 530 | 900 |

Summary: Total air-to-air U = 0.143 W/(m^2-K), R = 6.991 m^2-K/W, Wall UA = 9.097 W/K.

## Construction -- Roof (inside to outside)

| Layer | k [W/(m-K)] | Thickness [m] | U [W/(m^2-K)] | R [m^2-K/W] | Density [kg/m^3] | cp [J/(kg-K)] |
|-------|-------------|---------------|----------------|-------------|-------------------|---------------|
| Plasterboard | 0.16 | 0.010 | 16.000 | 0.063 | 950 | 840 |
| **Fiberglass quilt** | **0.04** | **0.400** | **0.100** | **10.000** | **12** | **840** |
| Roofdeck | 0.14 | 0.019 | 7.368 | 0.136 | 530 | 900 |

Summary: Total air-to-air U = 0.092 W/(m^2-K), R = 10.832 m^2-K/W, Roof UA = 4.431 W/K.

## Summary (Case 680 vs. Case 600)

| Component | UA [W/K] Case 600 | UA [W/K] Case 680 |
|-----------|-------------------|-------------------|
| Wall | 26.598 | 9.097 |
| Floor | 1.867 | 1.867 |
| Roof | 13.237 | 4.431 |
| S. Window | 25.184 | 25.184 |
| Infiltration | 18.555 | 18.555 |
| **Total** | **85.440** | **59.134** |

Internal heat capacity: 2344 kJ/K (vs. 2024 kJ/K in Case 600, due to thicker insulation).

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- Additional output specified for Case 680 in Section 6.2.1.8
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- The increased insulation substantially reduces the building envelope losses.
- Note the change from fiberglass quilt to foam insulation in walls (different density and specific heat).
- The floor construction is unchanged from Case 600.
