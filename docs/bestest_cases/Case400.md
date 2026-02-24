# Case 400: High-Conductance Wall Elements with Deadband Thermostat

## Overview

Case 400 is the base case for the in-depth diagnostic series with "20,27" deadband thermostat. It is derived from Case 600 with modifications similar to Case 220 but using the deadband thermostat. The standard reference is ASHRAE 140, Section 5.2.3.15.

## Base Case

Based on Case 600, with the following changes.

## Changes from Case 600

- Infiltration rate = 0 ach (no infiltration)
- Internal gains = 0 W (no internal heat generation)
- Exterior solar absorptance = 0.1 (all opaque surfaces including HC wall elements; raised floor exterior receives no solar radiation)
- South-facing windows (12 m^2) replaced by high-conductance wall elements (as in Case 220, Section 5.2.3.1.4)
- High-conductance wall elements also have exterior solar absorptance = 0.1
- Thermostat: "20,27" deadband (as in Case 600)

## Construction

### High-Conductance Wall Element

Same as Case 220 (Section 5.2.3.1.4):
- Two units, each 3 m x 2 m
- Opaque panel / air gap / opaque panel construction
- Shortwave transmittance = 0
- Total air-to-air U = 2.10 W/(m^2-K)

## Surface Properties

| Property | Interior Surface | Exterior Surface |
|----------|-----------------|------------------|
| Solar absorptance | 0.6 (opaque surfaces) | 0.1 |
| Infrared emittance | 0.9 | 0.9 |

## HVAC

- Heat = ON if temperature < 20 C; otherwise Heat = OFF
- Cool = ON if temperature > 27 C; otherwise Cool = OFF
- Nonproportional thermostat as in Case 600

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Case 400 is essentially Case 220 but with the deadband (20,27) thermostat instead of the (20,20) thermostat.
- Comparing Cases 400 and 395 tests surface convection and IR radiation (similar to Cases 200 and 195).
- The high-conductance wall elements are identical to those in Case 220.
