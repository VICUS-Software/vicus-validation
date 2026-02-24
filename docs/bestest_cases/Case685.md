# Case 685: Base Case with "20,20" Thermostat

## Base Case

Based on Case 600, with a modified thermostat control strategy.

## Changes from Case 600

- The deadband thermostat (20,27) is replaced with a single-setpoint thermostat (20,20):
  - Heat = ON if temperature < 20 C
  - Cool = ON if temperature > 20 C
- All other parameters remain as in Case 600.

## HVAC

### Thermostat Control

- Heat = ON if temperature < 20 C; otherwise Heat = OFF
- Cool = ON if temperature > 20 C; otherwise Cool = OFF
- Nonproportional thermostat as in Case 600 (Section 5.2.1.13.1.2)

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- Additional output specified for Case 685 in Section 6.2.1.8
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- The only change from Case 600 is the thermostat: no deadband, single setpoint at 20 C for both heating and cooling.
- This eliminates the 7 C deadband between heating and cooling, resulting in higher cooling loads and different peak load characteristics.
- This thermostat strategy is also used in the in-depth diagnostic series (Cases 220--320).
