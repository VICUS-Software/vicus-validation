# Case 810: High-Mass Cavity Albedo

## Base Case

Based on Case 900, with reduced interior solar absorptance.

## Changes from Case 900

- Interior shortwave absorptance = 0.1 (as in Case 280), applied to the interior side of all opaque surfaces.
- Interior solar distribution shall be as specified in Section 5.2.3.10.2 (Case 280).
- All other parameters remain as in Case 900.

## Surface Properties

| Property | Interior Surface | Exterior Surface |
|----------|-----------------|------------------|
| Solar absorptance | **0.1** | 0.6 |
| Infrared emittance | 0.9 | 0.9 |

## Interior Solar Distribution (from Case 280)

| Surface | Floor | Ceiling | East Wall | West Wall | North Wall | South Wall | Solar Lost through Windows |
|---------|-------|---------|-----------|-----------|------------|------------|--------------------------|
| Fraction | 0.243 | 0.191 | 0.057 | 0.057 | 0.077 | 0.063 | 0.312 |

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Case 810 tests the effect of cavity albedo (low interior solar absorptance) in combination with high thermal mass.
- Comparing Cases 810 and 900 isolates the effect of interior solar absorptance on a high-mass building.
- The low interior absorptance significantly increases the fraction of solar radiation lost back through the windows (0.312 vs. 0.035 in Case 600/900 with absorptance 0.6).
