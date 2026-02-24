# Case 430: Exterior Shortwave Absorptance (Deadband Thermostat)

## Base Case

Based on Case 420, with increased exterior shortwave absorptance.

## Changes from Case 420

- Exterior shortwave (solar) absorptance = 0.6 (as in Case 600), applied to all opaque surfaces including the high-conductance wall elements.
- For the raised floor, the exterior surface continues to receive no solar radiation.
- All other parameters remain as in Case 420 (200 W internal gains, 0.5 ach, 20,27 thermostat).

## Surface Properties

| Property | Interior Surface | Exterior Surface |
|----------|-----------------|------------------|
| Solar absorptance | 0.6 | **0.6** |
| Infrared emittance | 0.9 | 0.9 |

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Comparing Cases 430 and 420 isolates the effect of exterior solar absorptance (0.6 vs. 0.1) with all other standard parameters present.
- This returns the exterior absorptance to the Case 600 value, testing incident solar radiation effects on opaque surfaces.
