# Case 610: South Shading (Overhang)

## Base Case

Based on Case 600, with the addition of a south window overhang.

## Changes from Case 600

- A horizontal overhang is added to the south-facing windows, extending across the entire length of the south wall.

## Shading Geometry

- Overhang depth: 1.0 m (projecting perpendicular from the south wall surface)
- Overhang height above window top: 0.5 m (i.e., overhang is at 2.7 m above floor level)
- Overhang extends across the entire 8 m length of the south wall

### Overhang Construction Properties

- Solar absorptance = 1 (reflectance = 0, transmittance = 0), independent of incidence angle
- Infrared emittance = 0
- All heat from solar radiation absorbed by the shading device is dissipated to the ambient environment via convection
- Both sides of the shading device actively shade the building
- Thickness: smallest allowable value (e.g., 0.001 m)

For properties with values of 0, apply the lowest value allowed by the program being tested (e.g., 0.0001).

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- Annual transmitted solar radiation through the shaded south window with horizontal overhang (kWh/m^2) -- this is optically transmitted only, not including glass-absorbed radiation conducted inward
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- The overhang must be modeled as an external shading device on the south wall.
- Ensure the overhang geometry matches the specification: 1.0 m depth, 0.5 m above window top, full south wall width.
- NANDRAD should calculate transmitted solar radiation through the shaded windows for comparison with reference values.
