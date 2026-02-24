# Case 220: In-Depth Series Base Case (High-Conductance Wall Elements)

## Overview

Case 220 is the base case for the in-depth diagnostic series with "20,20" thermostat. It is derived from Case 600 with several key modifications. The standard reference is ASHRAE 140, Section 5.2.3.1.

## Base Case

Based on Case 600, with the following changes.

## Changes from Case 600

- Infiltration rate = 0 ach (no infiltration)
- Internal gains = 0 W (no internal heat generation)
- Exterior solar absorptance = 0.1 (reduced from 0.6)
- Interior solar absorptance = 0.6 (unchanged)
- South-facing windows (12 m^2) replaced by high-conductance wall elements
- Thermostat changed to "20,20" (single setpoint, no deadband)

## Opaque Surface Radiative Properties

| Property | Interior Surface | Exterior Surface |
|----------|-----------------|------------------|
| Solar absorptance | 0.6 | 0.1 |
| Infrared emittance | 0.9 | 0.9 |

These properties also apply to the high-conductance wall elements. Since there are no solar gains to the zone (no windows, no internal gains), interior solar absorptance does not affect results.

## Construction -- High-Conductance Wall Element

The 12 m^2 of south-facing windows are replaced by two high-conductance wall elements (each 3 m x 2 m = 6 m^2). These elements have the same thermal and optical behavior as the double-pane window of Case 600, but with zero shortwave transmittance.

### Geometry

| Property | Value |
|----------|-------|
| Height, individual unit | 2 m |
| Width, individual unit | 3 m |
| Area, individual unit | 6 m^2 |
| Number of individual units | 2 |

### Fundamental Material Thermal Properties

| Layer | k [W/(m-K)] | Thickness [mm] | U [W/(m^2-K)] | R [m^2-K/W] | Density [kg/m^3] | cp [J/(kg-K)] |
|-------|-------------|---------------|----------------|-------------|-------------------|---------------|
| Opaque panel | 1.00 | 3.048 | 328 | 0.00305 | 2470 | 750 |
| Air gap | 0.0625 | 12.0 | 5.208 | 0.19200 | 1.292498 | 1006.103271 |
| Opaque panel | 1.00 | 3.048 | 328 | 0.00305 | 2470 | 750 |

Note: Air-gap properties are constant (not allowed to vary with temperature and pressure). The air-gap conductivity k = U x Thickness = 0.0625 W/(m-K); this is the effective constant air-gap conductivity including the effect of natural convection, as calculated by WINDOW 7 for the Case 600 clear double-pane window.

### Properties

- Shortwave transmittance = 0
- Solar absorptance and infrared emittance: as specified in Table 5-34
- Surface texture: very smooth (same as window glass), for both interior and exterior surfaces

### Calculated Properties

| Property | U [W/(m^2-K)] | R [m^2-K/W] |
|----------|---------------|-------------|
| Interior combined surface coefficient (hi) | 4.5 | 0.22222 |
| Total surface-to-surface | 5.048 | 0.19810 |
| Exterior combined surface coefficient (ho) | 17.8 | 0.05618 |
| Total air-to-air | 2.10 | 0.47650 |

## HVAC

### Thermostat Control ("20,20")

- Heat = ON if temperature < 20 C; otherwise Heat = OFF
- Cool = ON if temperature > 20 C; otherwise Cool = OFF
- Nonproportional thermostat as in Case 600

## Infiltration

- 0 ach (no infiltration)

## Internal Gains

- 0 W (no internal heat generation)

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- This is the base case for the diagnostic series. The high-conductance wall elements must be modeled carefully to match the specified thermal properties.
- With no windows, no infiltration, and no internal gains, the only heat transfer mechanisms are conduction through the envelope and surface radiation exchange.
- The "20,20" thermostat means the zone temperature will be maintained at exactly 20 C whenever possible.
- Alternative constant surface coefficients for high-conductance wall elements: h,conv,ext = 8.0, h,comb,ext = 17.8; h,conv,int = 2.4, h,comb,int = 4.5.
