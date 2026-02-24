# Case 695: Increased Exterior Wall and Roof Insulation with "20,20" Thermostat

## Base Case

Based on Case 680 (increased insulation), with the thermostat control from Case 685.

## Changes from Case 680

- The deadband thermostat (20,27) is replaced with a single-setpoint thermostat (20,20):
  - Heat = ON if temperature < 20 C
  - Cool = ON if temperature > 20 C
- All other parameters remain as in Case 680 (increased wall and roof insulation).

## HVAC

### Thermostat Control

- Heat = ON if temperature < 20 C; otherwise Heat = OFF
- Cool = ON if temperature > 20 C; otherwise Cool = OFF
- Nonproportional thermostat as in Case 600 (Section 5.2.1.13.1.2)

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- Additional output specified for Case 695 in Section 6.2.1.8
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- This case combines the increased insulation of Case 680 with the tighter thermostat control of Case 685.
- The combination of high insulation and no deadband tests the interaction between reduced envelope losses and thermostat sensitivity.
