# Case 250: Exterior Shortwave Absorptance

## Base Case

Based on Case 220, with increased exterior shortwave absorptance.

## Changes from Case 220

- Exterior shortwave (solar) absorptance = 0.9, applied to the exterior side of all opaque surfaces, including the high-conductance wall elements.
- For the raised floor, the exterior surface continues to be modeled as receiving no solar radiation (Section 5.2.1.5.1).
- All other parameters remain as in Case 220.

## Surface Properties

| Property | Interior Surface | Exterior Surface |
|----------|-----------------|------------------|
| Solar absorptance | 0.6 | **0.9** |
| Infrared emittance | 0.9 | 0.9 |

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Comparing Cases 250 and 220 isolates the effect of exterior solar absorptance (0.9 vs. 0.1).
- High exterior absorptance means more solar radiation is absorbed by the opaque exterior surfaces, increasing heat gain through the envelope.
