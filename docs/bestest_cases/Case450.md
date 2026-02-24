# Case 450: Constant Combined Interior and Exterior Surface Coefficients

## Base Case

Based on Case 600, with constant combined surface heat transfer coefficients applied.

## Changes from Case 600

- Constant interior combined surface coefficients (h,comb,int) from Table 5-46 are applied.
- Constant exterior combined surface coefficients (h,comb,ext) from Table 5-46 are applied.
- Time-step-varying calculation of surface heat transfer coefficients is prohibited.
- Use of constant values other than those of Table 5-46 is prohibited.
- All other parameters remain as in Case 600.

## Surface Coefficients (Table 5-46)

| Surface Type | Interior Combined h,comb,int [W/(m^2-K)] | Exterior Combined h,comb,ext [W/(m^2-K)] |
|-------------|----------------------------------------|----------------------------------------|
| Walls | 1.8 | 21.6 |
| Roof | 1.7 | 21.8 |
| Raised Floor | 3.7 | 5.2 |
| Windows | 4.5 | 17.8 |

These are the same values as h,comb,int in Table 5-9 (Case 600) and h,comb,ext in Table 5-7 (Case 600).

For programs that allow direct input of constant convective surface coefficients but not direct input of constant combined coefficients: enter the appropriate values from Table 5-46 as convective coefficients, and set respective surface emittances to 0 (or as low as the program allows).

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- The purpose of Case 450 is to isolate differences associated with varying surface interior and exterior surface convective heat transfer and radiative exchange models.
- Compare results of Case 450 with Cases 600, 460, and 470 to diagnose surface heat transfer modeling.
- Cases 450, 460, 470, and 600 test interior and exterior surface convective and IR heat transfer.
