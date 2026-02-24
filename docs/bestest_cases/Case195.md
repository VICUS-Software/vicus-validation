# Case 195: Solid Conduction Test

## Base Case

Based on Case 200 (both IR emittances at 0.1), with high-conductance wall elements replaced by standard lightweight exterior walls.

## Changes from Case 200

- The 12 m^2 of high-conductance wall elements on the south wall are replaced with lightweight exterior walls as specified in Table 5-2 (Case 600 wall construction: plasterboard + fiberglass quilt + wood siding).
- These replacement walls have:
  - Rough exterior surface and smooth interior surface (as per Tables 5-6 and 5-8 of Case 600)
  - Surface radiative properties and surface heat transfer characteristics as specified for the lightweight exterior walls of Case 200

## Surface Properties

Same as Case 200:

| Property | Interior Surface | Exterior Surface |
|----------|-----------------|------------------|
| Solar absorptance | 0.6 | 0.1 |
| Infrared emittance | 0.1 | 0.1 |

## Key Parameters

- Setpoints: 20,20
- Mass: Low (lightweight)
- Internal gains: 0 W
- Infiltration: 0 ach
- No windows and no high-conductance wall elements
- 100% normally insulated wall as specified for the lightweight case

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Case 195 tests solid conduction only. The major difference between Cases 200 and 195 comes from the high-conductance wall elements being replaced by well-insulated lightweight walls.
- Increased differences between codes will be from the different film (surface heat transfer) algorithms.
- With no windows, no infiltration, no internal gains, and low IR emittances, this is a very simplified conduction-only test.
