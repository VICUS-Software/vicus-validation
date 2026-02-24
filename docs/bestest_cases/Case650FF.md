# Case 650FF: Free-Float Night Ventilation

## Base Case

Based on Case 650 (night ventilation), with no mechanical heating or cooling.

## Changes from Case 650

- No mechanical heating or cooling of the building.
- The mechanical ventilation schedule from Case 650 remains:
  - From 1800 to 0700 hours: vent fan = ON
  - From 0700 to 1800 hours: vent fan = OFF
- Ventilation fan characteristics remain as in Case 650:
  - Vent fan capacity = 1700 standard m^3/h (13.12 ach)
  - Waste heat from fan = 0
  - Altitude adjustment applies if needed (1409 m^3/h / 10.87 ach for sea-level programs)
- Standard infiltration (0.5 ach) remains in addition to ventilation.

## Required Outputs

- All free-float case output per Section 6.2.1.6
- Daily hourly output specified for Case 650FF in Section 6.2.1.8
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- This combines the night ventilation of Case 650 with free-floating temperatures (no HVAC).
- The nighttime ventilation will bring the zone temperature closer to outdoor temperature at night, while daytime temperatures will rise without mechanical cooling.
