# Case 950: High-Mass Night Ventilation

## Base Case

Based on Case 650 (night ventilation), with high-mass construction from Case 900.

## Changes from Case 650

- Exterior wall and floor material properties are replaced with those from Case 900 (Table 5-27):
  - Walls: concrete block + foam insulation + wood siding
  - Floor: concrete slab + insulation
- Roof remains as in Case 600/650.
- Ventilation schedule, fan characteristics, and thermostat control remain exactly as in Case 650:
  - Night ventilation: 1700 m^3/h from 1800 to 0700
  - Heating always OFF
  - Cooling ON if T > 27 C, daytime only (0700--1800)
  - Infiltration 0.5 ach remains

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- This is the high-mass equivalent of Case 650 -- night ventilation with massive wall and floor construction.
- The high thermal mass makes night ventilation much more effective at reducing daytime cooling loads, as the mass can store the "coolth" from night ventilation.
