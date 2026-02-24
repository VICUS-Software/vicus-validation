# Case 600: Low-Mass Base Case

## Overview

Case 600 is the base case for the BESTEST low-mass building series. All other low-mass cases (610--695, 600FF, 650FF, 680FF) and many in-depth diagnostic cases are derived from this specification. The standard reference is ASHRAE 140, Section 5.2.1.

## Building Geometry

- Floor area: 48 m^2 (8 m x 6 m)
- Ceiling height: 2.7 m
- Interior air volume: 129.6 m^3
- Single story, rectangular prism
- Two south-facing windows, each 3 m wide x 2 m high (total glazing area: 12 m^2)
- Window sill height: 0.2 m above floor
- No shading devices

## Site and Weather Data

- Weather file: 725650TY.CSV (TMY3, Denver International Airport, Colorado)
- Latitude: 39.83 N, Longitude: 104.65 W
- Altitude: 1650 m above sea level
- Time zone: UTC-7 (Mountain Standard Time)
- Ground reflectance (albedo): 0.2
- Terrain category 3 (open terrain, scattered obstructions < 9 m)

## Construction -- Exterior Wall (inside to outside)

| Layer | k [W/(m-K)] | Thickness [m] | U [W/(m^2-K)] | R [m^2-K/W] | Density [kg/m^3] | cp [J/(kg-K)] |
|-------|-------------|---------------|----------------|-------------|-------------------|---------------|
| Plasterboard | 0.16 | 0.012 | 13.333 | 0.075 | 950 | 840 |
| Fiberglass quilt | 0.04 | 0.066 | 0.606 | 1.650 | 12 | 840 |
| Wood siding | 0.14 | 0.009 | 15.556 | 0.064 | 530 | 900 |

Summary: Total wall area = 63.6 m^2, UA = 26.598 W/K, Total air-to-air U = 0.418 W/(m^2-K), R = 2.391 m^2-K/W.

## Construction -- Raised Floor (inside to outside)

| Layer | k [W/(m-K)] | Thickness [m] | U [W/(m^2-K)] | R [m^2-K/W] | Density [kg/m^3] | cp [J/(kg-K)] |
|-------|-------------|---------------|----------------|-------------|-------------------|---------------|
| Timber flooring | 0.14 | 0.025 | 5.600 | 0.179 | 650 | 1200 |
| Insulation | 0.04 | 1.003 | 0.040 | 25.075 | ~0 | ~0 |

Summary: Floor area = 48.0 m^2, UA = 1.867 W/K, Total air-to-air U = 0.039 W/(m^2-K), R = 25.716 m^2-K/W. Underfloor insulation has minimum density and specific heat the program allows (but not < 0). The raised floor is exposed to outdoor air temperature below; the exterior floor surface receives no solar radiation and has zero wind speed.

## Construction -- Roof (inside to outside)

| Layer | k [W/(m-K)] | Thickness [m] | U [W/(m^2-K)] | R [m^2-K/W] | Density [kg/m^3] | cp [J/(kg-K)] |
|-------|-------------|---------------|----------------|-------------|-------------------|---------------|
| Plasterboard | 0.16 | 0.010 | 16.000 | 0.063 | 950 | 840 |
| Fiberglass quilt | 0.04 | 0.1118 | 0.358 | 2.794 | 12 | 840 |
| Roofdeck | 0.14 | 0.019 | 7.368 | 0.136 | 530 | 900 |

Summary: Roof area = 48.0 m^2, UA = 13.237 W/K, Total air-to-air U = 0.276 W/(m^2-K), R = 3.626 m^2-K/W.

## Windows

- Type: Clear double-pane glazing system
- Number of panes: 2
- Pane thickness: 3.048 mm each
- Air gap between panes: 12.0 mm
- Fill gas: Air
- No sash, frames, spacers, mullions, blinds, or curtains

### Glass Material Properties

- Thermal conductivity: 1.00 W/(m-K)
- Density: 2470 kg/m^3
- Specific heat: 750 J/(kg-K)
- Hemispherical infrared emittance: 0.840
- Infrared transmittance: 0.000
- Direct-beam transmittance per pane: 0.834 (at normal incidence)
- Direct-beam reflectance per pane: 0.075 (at normal incidence)

### Calculated Glazing System Properties

- Effective air gap conductance (hs): 5.208 W/(m^2-K)
- U-value (interior air to ambient air): 2.10 W/(m^2-K)
- SHGC: 0.769 (at normal incidence)
- Shading coefficient (SC): 0.883 (at normal incidence)
- South window UA = 25.184 W/K

### Angular-Dependent Optical Properties (Double-Pane)

| Angle [deg] | Trans. | Refl.,f | Refl.,b | Abs. Outer | Abs. Inner | SHGC |
|-------------|--------|---------|---------|------------|------------|------|
| 0 | 0.703 | 0.128 | 0.128 | 0.096 | 0.072 | 0.769 |
| 10 | 0.702 | 0.128 | 0.128 | 0.097 | 0.073 | 0.768 |
| 20 | 0.699 | 0.128 | 0.128 | 0.099 | 0.074 | 0.766 |
| 30 | 0.692 | 0.130 | 0.130 | 0.102 | 0.075 | 0.761 |
| 40 | 0.678 | 0.139 | 0.139 | 0.106 | 0.077 | 0.748 |
| 50 | 0.646 | 0.164 | 0.164 | 0.112 | 0.078 | 0.718 |
| 60 | 0.577 | 0.227 | 0.227 | 0.119 | 0.077 | 0.651 |
| 70 | 0.438 | 0.365 | 0.365 | 0.127 | 0.070 | 0.509 |
| 80 | 0.208 | 0.612 | 0.612 | 0.130 | 0.050 | 0.267 |
| 90 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 |
| Hemis. | 0.601 | 0.206 | 0.206 | 0.110 | 0.073 | 0.670 |

## Infiltration

- Rate: 0.5 ach, continuous (24 h/day, full year)
- Independent of wind speed, indoor/outdoor temperature difference, and other variables
- Altitude adjustment: if program assumes sea level, use 0.414 ach with factor 0.829

## Internal Gains

- 200 W, continuously (24 h/day, full year)
- 100% sensible, 0% latent
- Sensible split: 60% radiative, 40% convective

## Opaque Surface Radiative Properties

| Property | Interior Surface | Exterior Surface |
|----------|-----------------|------------------|
| Solar absorptance | 0.6 | 0.6 |
| Infrared emittance | 0.9 | 0.9 |

Raised floor exterior surface: modeled as receiving no solar radiation.

## Surface Heat Transfer Coefficients

### Exterior (Alternative Constant Combined Coefficients)

| Surface Type | h,conv,ext [W/(m^2-K)] | h,comb,ext [W/(m^2-K)] |
|-------------|----------------------|----------------------|
| Walls | 11.9 | 21.6 |
| Roof | 14.4 | 21.8 |
| Raised Floor | 0.8 | 5.2 |
| Windows | 8.0 | 17.8 |

### Interior (Alternative Constant Combined Coefficients)

| Surface Type | h,conv,int [W/(m^2-K)] | h,comb,int [W/(m^2-K)] |
|-------------|----------------------|----------------------|
| Walls | 2.2 | 1.8 |
| Ceiling | 1.8 | 1.7 |
| Raised Floor | 2.2 | 3.7 |
| Windows | 2.4 | 4.5 |

## Exterior Surface Texture

| Surface Type | Texture |
|-------------|---------|
| Walls | Rough |
| Roof | Rough |
| Raised Floor | Rough |
| Windows (glass) | Very Smooth |

## Interior Surface Texture

| Surface Type | Texture |
|-------------|---------|
| Walls | Smooth |
| Roof | Smooth |
| Raised Floor | Smooth |
| Windows (glass) | Very Smooth |

## Interior Solar Distribution

For programs that calculate interior solar distribution internally (via ray tracing), ignore the fractions below. For programs requiring explicit input:

| Surface | Floor | Ceiling | East Wall | West Wall | North Wall | South Wall | Solar Lost through Windows |
|---------|-------|---------|-----------|-----------|------------|------------|--------------------------|
| Fraction | 0.642 | 0.167 | 0.038 | 0.038 | 0.053 | 0.027 | 0.035 |

## HVAC / Mechanical System

- 100% convective air system
- Thermostat senses air temperature only
- Nonproportional thermostat
- No latent heat extraction
- Deadband thermostat control (20,27):
  - Heat = ON if temperature < 20 C; otherwise Heat = OFF
  - Cool = ON if temperature > 27 C; otherwise Cool = OFF
- Heating capacity: 1000 kW (effectively infinite), 100% efficient
- Cooling capacity: 1000 kW (effectively infinite), 100% efficient
- Sensible cooling only; no latent heat load calculation
- Waste heat from fan = 0

## Internal Mass

No additional internal mass (no furniture or unspecified elements).

## Required Outputs

- Annual heating load (MWh)
- Annual sensible cooling load (MWh)
- Annual peak heating load (kW) with month, day, hour
- Annual peak sensible cooling load (kW) with month, day, hour
- Annual incident unshaded total solar radiation on horizontal, north, east, south, west surfaces (kWh/m^2)
- Unshaded annual transmitted total solar radiation through south windows (kWh/m^2)
- Exterior and interior convective surface coefficients
- Sky temperature
- Monthly conditioned-zone loads (heating and cooling, kWh; peak heating and cooling, kW)
- Specific-day hourly output for incident/transmitted solar radiation and sky temperatures

## NANDRAD Modeling Notes

- Use the 20,27 deadband thermostat control strategy with ideal heating/cooling.
- Floor is modeled as a raised floor exposed to ambient air on the underside (zero wind speed, no solar radiation on exterior floor surface).
- Ensure the infiltration rate is adjusted for altitude (1650 m) if the program does not handle barometric pressure automatically.
- NANDRAD uses the TMY3 weather file (725650TY.CSV) converted to its .c6b climate format.
- Interior solar distribution should be handled by NANDRAD's internal algorithms if available; otherwise apply the fractions from Table 5-13.
