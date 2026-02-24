# Case 300: East/West Windows

## Base Case

Based on Case 270, with east/west window orientation.

## Changes from Case 270

- Window orientation is modified as in Case 620:
  - 6 m^2 of window area facing east
  - 6 m^2 of window area facing west
  - No south or north windows
- Windows are exactly as in Case 270 (Case 600 double-pane clear glazing).
- All other parameters remain as in Case 270 (interior absorptance 0.9, 0 infiltration, 0 internal gains).

## Interior Solar Distribution (Case 300)

| Surface | Floor | Ceiling | East Wall | West Wall | North Wall | South Wall | Solar Lost through Windows |
|---------|-------|---------|-----------|-----------|------------|------------|--------------------------|
| Fraction | 0.903 | 0.050 | 0.0065 | 0.0065 | 0.014 | 0.014 | 0.006 |

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Comparing Cases 300 and 270 isolates the effect of window orientation (east/west vs. south) on solar transmittance and incidence.
- East/west windows receive more solar radiation in summer and less in winter than south windows.
