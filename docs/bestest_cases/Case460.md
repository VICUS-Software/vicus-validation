# Case 460: Constant Combined Interior Surface Coefficients

## Base Case

Based on Case 600, with constant combined interior surface heat transfer coefficients applied.

## Changes from Case 600

- Constant interior combined surface coefficients (h,comb,int) from Table 5-46 (see Case 450, Section 5.2.3.21) are applied.
- Time-step-varying calculation of interior surface heat transfer coefficients is prohibited.
- Use of constant values other than those of Table 5-46 is prohibited.
- Exterior surface heat transfer remains as in Case 600 (Section 5.2.1.9).
- All other parameters remain as in Case 600.

## Interior Surface Coefficients (from Table 5-46)

| Surface Type | Interior Combined h,comb,int [W/(m^2-K)] |
|-------------|----------------------------------------|
| Walls | 1.8 |
| Roof | 1.7 |
| Raised Floor | 3.7 |
| Windows | 4.5 |

For programs that allow direct input of constant convective surface coefficients but not direct input of constant combined coefficients: enter the appropriate values from Table 5-46 as convective coefficients, and set respective interior surface emittances to 0 (or as low as the program allows).

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- The purpose of Case 460 is to isolate differences associated with varying interior surface convective heat transfer and radiative exchange models.
- Compare results of Cases 460, 450, and 600 to diagnose interior surface heat transfer.
