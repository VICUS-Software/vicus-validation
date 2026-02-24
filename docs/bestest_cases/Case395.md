# Case 395: Solid Conduction Test (Deadband Thermostat)

## Base Case

Based on Case 400, with high-conductance wall elements replaced by standard lightweight exterior walls.

## Changes from Case 400

- The 12 m^2 of high-conductance wall elements on the south wall are replaced with lightweight exterior walls as specified in Table 5-2 (Case 600 wall construction: plasterboard + fiberglass quilt + wood siding).
- These replacement walls have:
  - Rough exterior surface and smooth interior surface (as per Tables 5-6 and 5-8 of Case 600)
  - Surface radiative properties and surface heat transfer characteristics as specified for the lightweight exterior walls of Case 400

## Key Parameters

- Setpoints: 20,27 (deadband)
- Mass: Low (lightweight)
- Internal gains: 0 W
- Infiltration: 0 ach
- No windows and no high-conductance wall elements
- Exterior solar absorptance: 0.1
- Interior IR emittance: 0.9, Exterior IR emittance: 0.9

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Case 395 tests solid conduction with the deadband thermostat. It is the "20,27" equivalent of Case 195.
- Comparing Cases 400 and 395 tests surface convection and IR radiation. The major portion of the change in results between these cases comes from the high-conductance wall elements.
- Increased differences between codes will be from the different film convection and IR algorithms.
