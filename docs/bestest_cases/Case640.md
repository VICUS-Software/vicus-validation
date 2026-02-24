# Case 640: Thermostat Setback

## Base Case

Based on Case 600, with a modified heating thermostat schedule (night setback).

## Changes from Case 600

- The heating thermostat set point is reduced at night (setback schedule).
- Cooling thermostat remains unchanged.

## HVAC

### Thermostat Control Strategy

- **0800--2300 hours**: Heat = ON if temperature < 20 C; otherwise Heat = OFF
- **2300--0700 hours**: Heat = ON if temperature < 10 C; otherwise Heat = OFF
  - The 10 C setting beginning immediately after 2300 hours is an instantaneous step-down from the 20 C setting
- **0700--0800 hours**: The thermostat set point varies linearly from 10 C to 20 C
  - For programs with sub-hourly time steps: incremental linear ramp-up (e.g., for 15-min steps: 12.5, 15, 17.5, 20 C); heat is added so zone temperature at end of each sub-hourly step corresponds to the set point at that time, reaching 20 C at 0800
  - For programs with hourly time steps: if zone temperature < 20 C at 0700, heat is added during the hour 0700--0800 such that zone temperature = 20 C at 0800
- **All hours**: Cool = ON if temperature > 27 C; otherwise mechanical equipment is OFF
- Nonproportional thermostat as in Case 600

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- Daily hourly output as specified for Case 640 in Section 6.2.1.8
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- NANDRAD must implement the heating schedule with night setback (10 C from 2300 to 0700) and linear ramp-up (0700 to 0800).
- The instantaneous step-down at 2300 and linear ramp-up from 0700 to 0800 are critical for matching reference results.
- Cooling setpoint remains at 27 C continuously.
