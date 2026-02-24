# Case 670: Single-Pane Windows

## Base Case

Based on Case 600, with single-pane clear windows replacing the double-pane glazing.

## Changes from Case 600

- South-facing windows are replaced with single-pane clear glazing.
- All other parameters remain as in Case 600.

## Windows

### Fundamental Properties of Clear Single-Pane Glazing System

| Property | Value |
|----------|-------|
| Height, individual rough opening | 2 m |
| Width, individual rough opening | 3 m |
| Area, individual gross window | 6 m^2 |
| Number of panes | 1 |
| Pane thickness | 3.048 mm |
| Curtains, blinds, frames, etc. | None |

### Glass Material Properties

- Thermal conductivity: 1.00 W/(m-K)
- Density: 2470 kg/m^3
- Specific heat: 750 J/(kg-K)
- Hemispherical infrared emittance: 0.840
- Infrared transmittance: 0.000
- Direct-beam transmittance: 0.834, at normal incidence
- Direct-beam reflectance (same both sides): 0.075, at normal incidence

### Calculated Glazing System Properties

| Property | Value |
|----------|-------|
| Pane conductance | 328 W/(m^2-K) |
| Exterior combined surface coefficient (ho) | 16.0 W/(m^2-K) |
| Interior combined surface coefficient (hi) | 7.8 W/(m^2-K) |
| U-value (interior air to ambient air) | 5.16 W/(m^2-K) |
| SHGC | 0.864, at normal incidence |
| Shading coefficient (SC) | 0.993, at normal incidence |
| Index of refraction | 1.493 |
| Extinction coefficient | 0.0337/mm |
| South window UA | 61.935 W/K |
| Total building UA | 122.191 W/K |

### Angular-Dependent Optical Properties (Single-Pane Window)

| Angle [deg] | Trans. | Refl.,f | Refl.,b | Abs. | SHGC |
|-------------|--------|---------|---------|------|------|
| 0 | 0.834 | 0.075 | 0.075 | 0.091 | 0.864 |
| 10 | 0.833 | 0.075 | 0.075 | 0.092 | 0.864 |
| 20 | 0.831 | 0.075 | 0.075 | 0.094 | 0.862 |
| 30 | 0.827 | 0.077 | 0.077 | 0.096 | 0.859 |
| 40 | 0.818 | 0.082 | 0.082 | 0.100 | 0.851 |
| 50 | 0.797 | 0.099 | 0.099 | 0.104 | 0.831 |
| 60 | 0.749 | 0.143 | 0.143 | 0.108 | 0.785 |
| 70 | 0.637 | 0.253 | 0.253 | 0.110 | 0.673 |
| 80 | 0.389 | 0.506 | 0.506 | 0.105 | 0.424 |
| 90 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| Hemis. | 0.753 | 0.136 | 0.136 | 0.101 | 0.787 |

## Interior Solar Distribution (Case 670)

| Surface | Floor | Ceiling | East Wall | West Wall | North Wall | South Wall | Solar Lost through Windows |
|---------|-------|---------|-----------|-----------|------------|------------|--------------------------|
| Fraction | 0.641 | 0.166 | 0.038 | 0.038 | 0.052 | 0.025 | 0.040 |

## Required Outputs

- All non-free-float case output per Section 6.2.1.1
- Additional output per Section 6.2.1.2.2 (transmitted solar radiation)
- Daily hourly output as specified for Case 670 in Section 6.2.1.8
- Case-670-only output: annual hourly load-weighted average exterior and interior convective surface coefficients for the single-pane window (Section 6.2.1.10)
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- The single-pane window has a much higher U-value (5.16 vs. 2.10 W/(m^2-K)) and SHGC (0.864 vs. 0.769) than Case 600.
- This significantly increases both heat loss and solar gains.
- Total building UA more than doubles compared to Case 600 due to the window change.
