# Case 210: Interior Infrared Radiation Exchange

## Base Case

Based on Case 220, with reduced interior infrared radiation.

## Changes from Case 220

- Interior infrared emittance = 0.1 for all opaque surfaces, including the high-conductance wall elements.
- All other parameters remain as in Case 220.

## Surface Properties

| Property | Interior Surface | Exterior Surface |
|----------|-----------------|------------------|
| Solar absorptance | 0.6 | 0.1 |
| Infrared emittance | **0.1** | 0.9 |

## Alternative Constant Interior Surface Coefficients (Case 210)

For programs that do not calculate time-step-varying interior surface coefficients:

| Surface Type | h,conv,int [W/(m^2-K)] | h,comb,int [W/(m^2-K)] |
|-------------|----------------------|----------------------|
| Walls | 1.9 | 2.1 |
| Ceiling | 1.9 | 1.9 |
| Raised Floor | 1.0 | 0.4 |
| HC Wall Elements | 2.6 | 3.1 |

Note: h,comb,int <= h,conv,int is possible for floor and ceiling because convective and radiative heat flows may be in opposite directions.

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Comparing Cases 220 and 210 isolates the effect of interior infrared radiation exchange (IR emittance 0.9 vs. 0.1 interior).
- With low interior IR emittance, radiative heat exchange between interior surfaces is greatly reduced; heat transfer is dominated by convection.
