# Case 630: East/West Windows with Shading (Overhang + Fins)

## Base Case

Based on Case 620, with the addition of shading devices on east and west windows.

## Changes from Case 620

- Horizontal overhang and vertical fins are added to both east and west windows.

## Shading Geometry

### Overhang (each window)
- Depth: 1.0 m (projecting perpendicular from the wall surface)
- Height above window top: 0.5 m
- Width: extends across the full 3 m window width plus 0.5 m on each side (total 4 m)

### Vertical Fins (each window)
- Depth: 1.0 m (projecting perpendicular from the wall surface)
- Distance from window edge to fin: 0.0 m (fins flush with window edges)
- Fins on both sides of each window
- Height: extends from overhang down to 0.5 m below window sill

### Shading Device Construction

Same as Case 610:
- Solar absorptance = 1 (reflectance = 0, transmittance = 0)
- Infrared emittance = 0
- All absorbed heat dissipated to ambient via convection
- Both sides actively shade the building
- Thickness: smallest allowable value (e.g., 0.001 m)

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- Annual transmitted solar radiation through the shaded west window with horizontal overhang and vertical fins (kWh/m^2)
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- This case combines Case 620 (east/west windows) with external shading devices (overhang + fins).
- The shading geometry must be modeled accurately for both east and west windows.
- Compare transmitted solar radiation through shaded west window against reference values to validate shading calculations.
