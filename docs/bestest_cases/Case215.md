# Case 215: Exterior Infrared Radiation Exchange

## Base Case

Based on Case 220, with reduced exterior infrared radiation.

## Changes from Case 220

- Exterior infrared emittance = 0.1 for all opaque surfaces, including the high-conductance wall elements.
- All other parameters remain as in Case 220.

## Surface Properties

| Property | Interior Surface | Exterior Surface |
|----------|-----------------|------------------|
| Solar absorptance | 0.6 | 0.1 |
| Infrared emittance | 0.9 | **0.1** |

## Alternative Constant Exterior Surface Coefficients (Case 215)

For programs that do not calculate time-step-varying exterior surface coefficients:

| Surface Type | h,conv,ext [W/(m^2-K)] | h,comb,ext [W/(m^2-K)] |
|-------------|----------------------|----------------------|
| Walls | 11.8 | 12.8 |
| Roof | 14.4 | 17.4 |
| Raised Floor | 0.9 | 1.3 |
| HC Wall Elements | 7.9 | 8.1 |

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Comparing Cases 220 and 215 isolates the effect of exterior infrared radiation exchange (IR emittance 0.9 vs. 0.1 exterior).
- With low exterior IR emittance, the exterior surface loses much less heat by longwave radiation to sky and ground.
