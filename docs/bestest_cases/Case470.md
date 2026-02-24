# Case 470: Constant Combined Exterior Surface Coefficients

## Base Case

Based on Case 600, with constant combined exterior surface heat transfer coefficients applied.

## Changes from Case 600

- Constant exterior combined surface coefficients (h,comb,ext) from Table 5-46 (see Case 450, Section 5.2.3.21) are applied.
- Time-step-varying calculation of exterior surface heat transfer coefficients is prohibited.
- Use of constant values other than those of Table 5-46 is prohibited.
- Interior surface heat transfer remains as in Case 600 (Section 5.2.1.10).
- All other parameters remain as in Case 600.

## Exterior Surface Coefficients (from Table 5-46)

| Surface Type | Exterior Combined h,comb,ext [W/(m^2-K)] |
|-------------|----------------------------------------|
| Walls | 21.6 |
| Roof | 21.8 |
| Raised Floor | 5.2 |
| Windows | 17.8 |

For programs that allow direct input of constant convective surface coefficients but not direct input of constant combined coefficients: enter the appropriate values from Table 5-46 as convective coefficients, and set respective exterior surface emittances to 0 (or as low as the program allows).

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- The purpose of Case 470 is to isolate differences associated with varying exterior surface convective heat transfer and radiative exchange models.
- Compare results of Cases 470, 450, and 600 to diagnose exterior surface heat transfer.
