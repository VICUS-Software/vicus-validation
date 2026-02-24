# Case 230: Infiltration

## Base Case

Based on Case 220, with infiltration added.

## Changes from Case 220

- Infiltration rate = 1.0 ach, continuously (24 hours per day, full year).
- Infiltration is independent of wind speed, indoor/outdoor temperature difference, and other variables.
- All other parameters remain as in Case 220.

## Infiltration

- Rate: 1.0 ach (double the Case 600 rate of 0.5 ach)
- Altitude adjustment: if the program assumes sea level, use 0.829 ach with adjustment factor 0.829.
- The calculation technique for altitude adjustment is described in Annex B3, Section B3.1.

## Required Outputs

- Non-free-float case output per Section 6.2.1.1
- General reporting requirements of Section 6.1

## NANDRAD Modeling Notes

- Comparing Cases 230 and 220 isolates the effect of infiltration (1.0 ach vs. 0 ach).
- The altitude correction must be applied consistently.
