# Case 985: High Mass with "20,20" Thermostat

## Base Case

Based on Case 900, with a modified thermostat control strategy.

## Changes from Case 900

- The deadband thermostat (20,27) is replaced with a single-setpoint thermostat (20,20):
  - Heat = ON if temperature < 20 C
  - Cool = ON if temperature > 20 C
- All other parameters remain as in Case 900.

## HVAC

### Thermostat Control

- Heat = ON if temperature < 20 C; otherwise Heat = OFF
- Cool = ON if temperature > 20 C; otherwise Cool = OFF
- Nonproportional thermostat as in Case 600 (Section 5.2.1.13.1.2), also applied in Case 685.

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- Additional output specified for Case 985 in Section 6.2.1.8
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- This is the high-mass equivalent of Case 685 -- single setpoint thermostat at 20 C with massive construction.
- The high thermal mass will significantly affect how the building responds to the tighter temperature control.
