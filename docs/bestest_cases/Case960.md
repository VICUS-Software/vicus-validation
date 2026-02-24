# Case 960: Sunspace

## Base Case

Based on Case 600 (back zone) and Case 900 (sun zone construction), this is a two-zone case with a sunspace.

## Changes from Case 600

- The building is divided into two zones (back zone and sun zone) separated by a common wall.
- The back zone is lightweight construction (as Case 600).
- The sun zone is heavyweight construction (as Case 900).

## Building Geometry

### Back Zone
- Dimensions: 8 m wide x 6 m deep x 2.7 m high
- The south wall and windows of Case 600 are replaced by the common wall.
- All other walls, roof, and floor are the same as Case 600.

### Sun Zone
- Dimensions: 8 m wide x 2 m deep x 2.7 m high
- North wall is replaced by the common wall.
- South wall has two 3 m x 2 m windows (same as Case 900, but raised 0.3 m higher on the south wall).
- East and west wall areas: 5.4 m^2 each.
- Air volume: 43.2 m^3.
- Thermal and physical properties: same as Case 900.

### Sun-Zone/Back-Zone Common Wall

| k [W/(m-K)] | Thickness [m] | U [W/(m^2-K)] | R [m^2-K/W] | Density [kg/m^3] | cp [J/(kg-K)] | Solar Absorptance | IR Emittance |
|-------------|---------------|----------------|-------------|-------------------|---------------|-------------------|-------------|
| 0.510 | 0.20 | 2.55 | 0.392 | 1400 | 1000 | 0.6 | 0.9 |

U-values and R-values are surface-to-surface (excluding interior surface heat transfer coefficients).

## Infiltration

- Back zone: 0.5 ach (exchange with ambient air only, no interzonal)
- Sun zone: 0.5 ach (exchange with ambient air only, no interzonal)
- Altitude adjustment applies as in Case 600.

## Internal Gains

- Back zone: 200 W, continuously (same as Case 600)
- Sun zone: 0 W

## Interior Solar Distribution (Sun Zone)

| Surface | Floor | Ceiling | East Wall | West Wall | North Wall | South Wall | Solar Lost through Windows |
|---------|-------|---------|-----------|-----------|------------|------------|--------------------------|
| Fraction | 0.6 | 0.05 | 0.02 | 0.02 | 0.2 | 0.03 | 0.08 |

## HVAC

- Sun zone: no space-conditioning system; temperature is free-floating.
- Back zone: controlled the same as Case 600 (20,27 deadband thermostat).

## Interzone Mass Transfer

No mechanically-driven or natural interzone air exchange.

## Required Outputs

- Back zone only: all non-free-float case outputs per Section 6.2.1.1
- Sun zone only: all free-float case outputs per Section 6.2.1.6
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- This is the only two-zone case in the BESTEST suite. NANDRAD must model two separate thermal zones with a common wall.
- No air exchange between zones -- they are thermally coupled only through the common wall.
- The sun zone acts as a passive solar collector, warming through the south-facing windows and transferring heat to the back zone through the common wall.
