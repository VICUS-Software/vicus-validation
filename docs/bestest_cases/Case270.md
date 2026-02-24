# Case 270: South Solar Gains

## Base Case

Based on Case 220, with south-facing transparent windows added.

## Changes from Case 220

- Interior shortwave absorptance = 0.9 (applied to interior side of all opaque surfaces only).
- The 12 m^2 of high-conductance wall elements on the south wall are replaced by transparent windows as in Case 600:
  - Window geometry: as shown in Figure 5-1 (Case 600)
  - Window thermal and optical properties: as in Section 5.2.1.11 (Case 600 double-pane clear glazing)
- Exterior and interior surface radiation and convection for windows: as specified in Sections 5.2.1.9 and 5.2.1.10 (Case 600)
- All other parameters remain as in Case 220 (0 ach infiltration, 0 W internal gains, exterior absorptance 0.1)

## Surface Properties

| Property | Interior Surface | Exterior Surface |
|----------|-----------------|------------------|
| Solar absorptance | **0.9** | 0.1 |
| Infrared emittance | 0.9 | 0.9 |

## Interior Solar Distribution (Case 270)

| Surface | Floor | Ceiling | East Wall | West Wall | North Wall | South Wall | Solar Lost through Windows |
|---------|-------|---------|-----------|-----------|------------|------------|--------------------------|
| Fraction | 0.903 | 0.050 | 0.010 | 0.010 | 0.014 | 0.007 | 0.006 |

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Comparing Cases 270 and 220 isolates the effect of south solar gains through transparent windows (solar transmittance and incidence).
- The high interior solar absorptance (0.9) maximizes solar absorption on interior surfaces.
- With 0 infiltration and 0 internal gains, only solar gains and envelope conduction determine loads.
