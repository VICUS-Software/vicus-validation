# Case 200: Interior and Exterior Infrared Radiation Exchange

## Base Case

Based on Case 210 (reduced interior IR), with additionally reduced exterior infrared radiation.

## Changes from Case 210

- Exterior infrared emittance = 0.1 for all opaque surfaces, including the high-conductance wall elements.
- Interior infrared emittance remains 0.1 (as in Case 210).
- All other parameters remain as in Case 210.

## Surface Properties

| Property | Interior Surface | Exterior Surface |
|----------|-----------------|------------------|
| Solar absorptance | 0.6 | 0.1 |
| Infrared emittance | **0.1** | **0.1** |

## Alternative Constant Exterior Surface Coefficients

Same as Case 215 (Section 5.2.3.3.2).

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- Case-200-only output per Section 6.2.1.9: annual hourly load-weighted average exterior and interior convective surface coefficients for the roof, north/east/west/south walls, and high-conductance wall element
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Comparing Cases 210, 200, and 215 isolates interior IR (Cases 220 vs. 210), exterior IR (Cases 215 vs. 200), and combined IR effects.
- With both interior and exterior IR emittance at 0.1, longwave radiation exchange is minimized; heat transfer is primarily convective.
- Run Cases 200--215 only if the program can explicitly adjust infrared emittance in the film convection algorithms.
