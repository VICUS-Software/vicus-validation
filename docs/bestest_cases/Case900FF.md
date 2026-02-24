# Case 900FF: Free-Float High Mass

## Base Case

Based on Case 900, with no mechanical heating or cooling.

## Changes from Case 900

- No mechanical heating or cooling of the building.
- All other parameters remain exactly as in Case 900.

## HVAC

- No mechanical system; the zone air temperature is free-floating.

## Required Outputs

- All free-float case output per Section 6.2.1.6:
  - Annual mean zone air temperature (C)
  - Annual hourly integrated minimum zone air temperature (C) with month, day, hour
  - Annual hourly integrated maximum zone air temperature (C) with month, day, hour
- Case 900FF only output per Section 6.2.1.7:
  - Annual hourly integrated 1 C zone air temperature bin frequencies from -50 C to 98 C
- Daily hourly output specified for Case 900FF in Section 6.2.1.8
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- The high thermal mass will result in significantly reduced temperature swings compared to Case 600FF.
- The temperature bin frequency output is unique to this case and requires post-processing 8760 hours of zone air temperature data.
