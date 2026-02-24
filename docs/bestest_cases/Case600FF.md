# Case 600FF: Free-Float Low Mass

## Base Case

Based on Case 600, with no mechanical heating or cooling.

## Changes from Case 600

- No mechanical heating or cooling of the building.
- All other parameters remain exactly as in Case 600.

## HVAC

- No mechanical system; the zone air temperature is free-floating.

## Required Outputs

- All free-float case output per Section 6.2.1.6:
  - Annual mean zone air temperature (C)
  - Annual hourly integrated minimum zone air temperature (C) with month, day, hour
  - Annual hourly integrated maximum zone air temperature (C) with month, day, hour
- Daily hourly output specified for Case 600FF in Section 6.2.1.8
- General reporting requirements of Section 6.1

The free-float zone air temperature is for the zone air only, assuming well-mixed air with no radiant effects (equivalent to an aspirated temperature sensor perfectly shielded from solar and infrared radiation).

## NANDRAD Modeling Notes

- Simply remove the ideal heating and cooling from the Case 600 model.
- This case tests the program's ability to predict zone air temperatures without any HVAC system.
- Temperature extremes (especially summer peaks) are important validation metrics.
