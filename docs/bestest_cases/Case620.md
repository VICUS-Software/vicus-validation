# Case 620: East/West Window Orientation

## Base Case

Based on Case 600, with modified window orientation.

## Changes from Case 600

- South-facing windows (2 x 6 m^2 = 12 m^2) are removed from the south wall.
- 6 m^2 of window area is placed on the east wall.
- 6 m^2 of window area is placed on the west wall.
- No windows on north or south walls.
- Window properties (glazing type, U-value, SHGC) are exactly as in Case 600.

## Windows

- East wall: one 3 m x 2 m window (6 m^2)
- West wall: one 3 m x 2 m window (6 m^2)
- Total glazing area: 12 m^2 (unchanged from Case 600)

## Interior Solar Distribution

For programs requiring explicit interior solar distribution fractions (Case 620 geometry):

| Surface | Floor | Ceiling | East Wall | West Wall | North Wall | South Wall | Solar Lost through Windows |
|---------|-------|---------|-----------|-----------|------------|------------|--------------------------|
| Fraction | 0.642 | 0.167 | 0.025 | 0.025 | 0.053 | 0.053 | 0.035 |

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- Unshaded annual transmitted total solar radiation through the west window (kWh/m^2)
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- The total glazing area remains 12 m^2 but is distributed equally on east and west walls instead of the south wall.
- Solar gains will differ significantly from Case 600 due to the changed window orientation.
- Ensure interior solar distribution fractions are updated if manually input.
