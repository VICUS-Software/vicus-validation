# Case 940: High-Mass Thermostat Setback

## Base Case

Based on Case 640 (thermostat setback), with high-mass construction from Case 900.

## Changes from Case 640

- Exterior wall and floor material properties are replaced with those from Case 900 (Table 5-27):
  - Walls: concrete block + foam insulation + wood siding
  - Floor: concrete slab + insulation
- Roof remains as in Case 600/640.
- Thermostat setback schedule remains exactly as in Case 640:
  - 0800--2300: Heat ON if T < 20 C
  - 2300--0700: Heat ON if T < 10 C (instantaneous step-down at 2300)
  - 0700--0800: Linear ramp from 10 C to 20 C
  - All hours: Cool ON if T > 27 C

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- This is the high-mass equivalent of Case 640 -- thermostat setback with massive construction.
- The high thermal mass will reduce the temperature drop during the night setback period and alter the morning recovery behavior compared to Case 640.
