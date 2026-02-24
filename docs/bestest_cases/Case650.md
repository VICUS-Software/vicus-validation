# Case 650: Night Ventilation

## Base Case

Based on Case 600, with a modified HVAC strategy: night ventilation cooling replaces mechanical cooling, and heating is disabled.

## Changes from Case 600

- Heating is always OFF.
- Mechanical cooling operates only during daytime (0700--1800) when temperature > 27 C.
- Nighttime ventilation fan operates from 1800 to 0700.
- Standard infiltration (0.5 ach) remains in addition to ventilation.

## HVAC

### Thermostat and Ventilation Fan Control Strategy

- **1800--0700 hours**: Vent fan = ON
- **0700--1800 hours**: Vent fan = OFF
- **Heating** = always OFF
- **1800--0700 hours**: Cool = OFF
- **0700--1800 hours**: Cool = ON if temperature > 27 C; otherwise Cool = OFF
- Nonproportional thermostat as in Case 600

### Ventilation Fan Characteristics

- Vent fan capacity = 1700 standard m^3/h (in addition to the 0.5 ach infiltration of Case 600)
  - Equivalent to 13.12 ach
- Waste heat from fan = 0
- If the program does not automatically correct for altitude:
  - Adjusted fan capacity = 1409 m^3/h (= 1700 x 1.0156/1.2255)
  - Adjusted ach = 10.87

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- This case tests the program's ability to model scheduled ventilation and the absence of heating.
- The ventilation rate (1700 m^3/h) is very large relative to the zone volume and operates only at night.
- Ensure the infiltration (0.5 ach) is maintained in addition to the ventilation fan airflow.
- The altitude correction for ventilation airflow must be applied consistently with the infiltration correction.
