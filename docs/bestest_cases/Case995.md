# Case 995: High-Mass Increased Exterior Wall and Roof Insulation with "20,20" Thermostat

## Base Case

Based on Case 980 (high-mass increased insulation), with the thermostat control from Case 985.

## Changes from Case 980

- The deadband thermostat (20,27) is replaced with a single-setpoint thermostat (20,20):
  - Heat = ON if temperature < 20 C
  - Cool = ON if temperature > 20 C
- All other parameters remain as in Case 980 (high-mass, increased wall and roof insulation).

## HVAC

### Thermostat Control

- Heat = ON if temperature < 20 C; otherwise Heat = OFF
- Cool = ON if temperature > 20 C; otherwise Cool = OFF
- Nonproportional thermostat as in Case 600 (Section 5.2.1.13.1.2), also applied in Case 685.

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- Additional output specified for Case 995 in Section 6.2.1.8
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- This case combines high thermal mass, increased insulation, and the tighter (20,20) thermostat.
- It is the high-mass equivalent of Case 695.
