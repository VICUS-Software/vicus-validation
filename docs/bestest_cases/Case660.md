# Case 660: Low-Emissivity Windows with Argon Gas

## Base Case

Based on Case 600, with different window glazing (low-emissivity argon-filled double pane).

## Changes from Case 600

- South-facing windows are replaced with low-emissivity argon-filled double-pane glazing.
- All other parameters remain as in Case 600.

## Windows

### Fundamental Properties of Low-Emissivity Argon-Filled Glazing System

| Property | Value |
|----------|-------|
| Height, individual rough opening | 2 m |
| Width, individual rough opening | 3 m |
| Area, individual gross window | 6 m^2 |
| Number of panes | 2 |
| Outer (low-e) pane thickness | 3.180 mm |
| Inner (clear) pane thickness | 3.048 mm |
| Thickness of space between panes | 12.0 mm |
| Fill gas | Argon |
| Curtains, blinds, frames, etc. | None |

### Glass Material Properties

- Thermal conductivity of glass: 1.00 W/(m-K)
- Density of glass: 2470 kg/m^3
- Specific heat of glass: 750 J/(kg-K)
- Hemispherical infrared emittance of glass: 0.840 (except outer pane inside facing surface)
- Outer pane inside facing surface infrared emittance: 0.047
- Infrared transmittance of glass: 0.000

### Argon Gas Properties (at 0 C, 101.325 kPa)

- Conductivity: 0.016349 W/(m-K)
- Specific heat: 521.928528 J/(kg-K)
- Density: 1.782282 kg/m^3
- Viscosity: 0.000021 kg/(m-s)
- Prandtl number: 0.6704
- Molecular weight: 39.948 g/mol

All argon properties may vary with temperature and pressure.

### Pane Optical Properties (at normal incidence)

| Property | Outer Pane (low-e) | Inner Pane (clear) |
|----------|-------------------|-------------------|
| Direct-beam transmittance | 0.452 | 0.834 |
| Direct-beam reflectance, outside facing | 0.359 | 0.075 |
| Direct-beam reflectance, inside facing | 0.397 | 0.075 |

### Calculated Glazing System Properties

| Property | Value |
|----------|-------|
| Effective conductance of argon gap (hs) | 1.792 W/(m^2-K) |
| U-value (interior air to ambient air) | 1.19 W/(m^2-K) |
| SHGC | 0.440, at normal incidence |
| Shading coefficient (SC) | 0.506, at normal incidence |
| South window UA | 14.239 W/K |
| Total building UA | 74.495 W/K |

### Angular-Dependent Optical Properties (Low-Emissivity Window)

| Angle [deg] | Trans. | Refl.,f | Refl.,b | Abs. Outer | Abs. Inner | SHGC |
|-------------|--------|---------|---------|------------|------------|------|
| 0 | 0.394 | 0.380 | 0.349 | 0.195 | 0.031 | 0.440 |
| 10 | 0.397 | 0.375 | 0.344 | 0.197 | 0.031 | 0.443 |
| 20 | 0.391 | 0.374 | 0.342 | 0.204 | 0.031 | 0.438 |
| 30 | 0.383 | 0.376 | 0.342 | 0.209 | 0.032 | 0.432 |
| 40 | 0.373 | 0.384 | 0.347 | 0.211 | 0.032 | 0.422 |
| 50 | 0.353 | 0.398 | 0.360 | 0.215 | 0.033 | 0.403 |
| 60 | 0.310 | 0.427 | 0.393 | 0.230 | 0.032 | 0.361 |
| 70 | 0.228 | 0.496 | 0.476 | 0.247 | 0.029 | 0.278 |
| 80 | 0.108 | 0.658 | 0.652 | 0.213 | 0.021 | 0.148 |
| 90 | 0.000 | 0.999 | 1.000 | 0.001 | 0.000 | 0.000 |
| Hemis. | 0.329 | 0.415 | 0.384 | 0.215 | 0.031 | 0.377 |

## Interior Solar Distribution (Case 660)

| Surface | Floor | Ceiling | East Wall | West Wall | North Wall | South Wall | Solar Lost through Windows |
|---------|-------|---------|-----------|-----------|------------|------------|--------------------------|
| Fraction | 0.645 | 0.170 | 0.039 | 0.039 | 0.054 | 0.026 | 0.027 |

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- Additional output per Section 6.2.1.2.2 (transmitted solar radiation)
- Daily hourly output as specified for Case 660 in Section 6.2.1.8
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- The low-e coating on the outer pane significantly reduces the U-value and SHGC compared to Case 600.
- The argon fill gas has different thermal properties than air, affecting the gap conductance.
- Ensure the asymmetric pane properties are correctly modeled (low-e outer pane vs. clear inner pane).
