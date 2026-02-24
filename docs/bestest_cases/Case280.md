# Case 280: Cavity Albedo (Interior Solar Absorptance)

## Base Case

Based on Case 270, with reduced interior solar absorptance.

## Changes from Case 270

- Interior shortwave absorptance = 0.1 (reduced from 0.9), applied to the interior side of all opaque surfaces.
- All other parameters remain as in Case 270 (south windows, 0 infiltration, 0 internal gains).

## Surface Properties

| Property | Interior Surface | Exterior Surface |
|----------|-----------------|------------------|
| Solar absorptance | **0.1** | 0.1 |
| Infrared emittance | 0.9 | 0.9 |

## Interior Solar Distribution (Case 280)

| Surface | Floor | Ceiling | East Wall | West Wall | North Wall | South Wall | Solar Lost through Windows |
|---------|-------|---------|-----------|-----------|------------|------------|--------------------------|
| Fraction | 0.243 | 0.191 | 0.057 | 0.057 | 0.077 | 0.063 | 0.312 |

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Comparing Cases 280 and 270 isolates the effect of interior solar absorptance (cavity albedo): 0.1 vs. 0.9.
- Low interior absorptance means most solar radiation is reflected multiple times within the zone, with a large fraction eventually lost back through the windows (0.312 vs. 0.006).
- This dramatically changes the effective solar heat gain of the building.
