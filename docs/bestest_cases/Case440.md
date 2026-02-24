# Case 440: Cavity Albedo (Deadband Thermostat)

## Base Case

Based on Case 600, with reduced interior solar absorptance.

## Changes from Case 600

- Interior shortwave absorptance = 0.1 (as in Case 280), applied to the interior side of all opaque surfaces.
- All other parameters remain as in Case 600.

## Surface Properties

| Property | Interior Surface | Exterior Surface |
|----------|-----------------|------------------|
| Solar absorptance | **0.1** | 0.6 |
| Infrared emittance | 0.9 | 0.9 |

## Interior Solar Distribution

As specified in Section 5.2.3.10.2 (Case 280):

| Surface | Floor | Ceiling | East Wall | West Wall | North Wall | South Wall | Solar Lost through Windows |
|---------|-------|---------|-----------|-----------|------------|------------|--------------------------|
| Fraction | 0.243 | 0.191 | 0.057 | 0.057 | 0.077 | 0.063 | 0.312 |

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Comparing Cases 440 and 600 isolates the effect of interior solar absorptance (cavity albedo): 0.1 vs. 0.6.
- Low interior absorptance significantly increases the solar radiation lost back through the windows (0.312 vs. 0.035), reducing effective solar heat gain.
