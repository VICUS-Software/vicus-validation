# Case 900: High-Mass Base Case

## Overview

Case 900 is the base case for the BESTEST high-mass building series. All other high-mass cases (910--995, 900FF, 950FF, 980FF) are derived from this specification. It is identical to Case 600 except that the exterior wall and floor use massive construction (concrete block walls, concrete slab floor). The roof remains the same as Case 600. The standard reference is ASHRAE 140, Section 5.2.2.2.1.

## Base Case

Based on Case 600, with changes to wall and floor material properties only.

## Changes from Case 600

- Exterior walls: concrete block + foam insulation + wood siding (replaces plasterboard + fiberglass + wood siding)
- Raised floor: concrete slab + insulation (replaces timber flooring + insulation)
- Roof: unchanged from Case 600
- All surface textures: unchanged from Case 600
- All other parameters (geometry, windows, infiltration, internal gains, HVAC, etc.): unchanged from Case 600

## Construction -- Exterior Wall (inside to outside)

| Layer | k [W/(m-K)] | Thickness [m] | U [W/(m^2-K)] | R [m^2-K/W] | Density [kg/m^3] | cp [J/(kg-K)] |
|-------|-------------|---------------|----------------|-------------|-------------------|---------------|
| Concrete Block | 0.51 | 0.100 | 5.100 | 0.196 | 1400 | 1000 |
| Foam Insulation | 0.04 | 0.0615 | 0.651 | 1.537 | 10 | 1400 |
| Wood Siding | 0.14 | 0.009 | 15.556 | 0.064 | 530 | 900 |

Summary: Total wall area = 63.6 m^2, UA = 26.509 W/K, Total air-to-air U = 0.417 W/(m^2-K), R = 2.399 m^2-K/W.

## Construction -- Raised Floor (inside to outside)

| Layer | k [W/(m-K)] | Thickness [m] | U [W/(m^2-K)] | R [m^2-K/W] | Density [kg/m^3] | cp [J/(kg-K)] |
|-------|-------------|---------------|----------------|-------------|-------------------|---------------|
| Concrete Slab | 1.13 | 0.080 | 14.125 | 0.071 | 1400 | 1000 |
| Insulation | 0.04 | 1.007 | 0.040 | 25.175 | ~0 | ~0 |

Summary: Floor area = 48.0 m^2, UA = 1.867 W/K, Total air-to-air U = 0.039 W/(m^2-K), R = 25.708 m^2-K/W. Floor insulation thickness varies slightly from Case 600 so total floor R-values match better.

## Construction -- Roof (inside to outside)

Same as Case 600:

| Layer | k [W/(m-K)] | Thickness [m] | U [W/(m^2-K)] | R [m^2-K/W] | Density [kg/m^3] | cp [J/(kg-K)] |
|-------|-------------|---------------|----------------|-------------|-------------------|---------------|
| Plasterboard | 0.16 | 0.010 | 16.000 | 0.063 | 950 | 840 |
| Fiberglass quilt | 0.04 | 0.1118 | 0.358 | 2.794 | 12 | 840 |
| Roofdeck | 0.14 | 0.019 | 7.368 | 0.136 | 530 | 900 |

## Summary Thermal Conductances and Heat Capacities

| Component | Area [m^2] | UA [W/K] | Internal Heat Capacity [kJ/K] | Total Heat Capacity [kJ/K] |
|-----------|-----------|----------|-------------------------------|---------------------------|
| Wall | 63.6 | 26.509 | 8959 | 9232 |
| Floor | 48.0 | 1.867 | 5376 | 5376 |
| Roof | 48.0 | 13.237 | 437 | 872 |
| S. Window | 12.0 | 25.184 | -- | -- |
| Infiltration | -- | 18.555 | -- | -- |
| **Total** | -- | **85.351** | **14772** | **15480** |

Total building UA = 85.351 W/K, Volume = 129.6 m^3, Air density = 1.0156 kg/m^3, cp = 1015 J/(kg-K).

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- Monthly conditioned-zone loads per Section 6.2.1.2.5
- Additional output specified for Case 900 in Section 6.2.1.8
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- The key difference from Case 600 is the thermal mass in walls and floor. Ensure concrete block and concrete slab layers are modeled with correct thickness, density, and specific heat.
- The roof construction is identical to Case 600.
- All other parameters (windows, infiltration, internal gains, HVAC, surface properties) remain as Case 600.
- The increased thermal mass significantly affects peak loads and temperature swings compared to Case 600.
