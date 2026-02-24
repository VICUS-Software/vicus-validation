# Case 320: "20,27" Deadband Thermostat with South Windows

## Base Case

Based on Case 270, with the thermostat changed to the deadband control of Case 600.

## Changes from Case 270

- The "20,20" thermostat is replaced with the "20,27" deadband thermostat (as in Case 600):
  - Heat = ON if temperature < 20 C; otherwise Heat = OFF
  - Cool = ON if temperature > 27 C; otherwise Cool = OFF
- Nonproportional thermostat as in Case 600.
- All other parameters remain as in Case 270 (south windows, interior absorptance 0.9, 0 infiltration, 0 internal gains).

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Comparing Cases 320 and 270 isolates the effect of the thermostat deadband (20,27 vs. 20,20).
- The 7 C deadband will eliminate some cooling load that exists in Case 270 when the zone temperature is between 20 C and 27 C.
