# Quiz SolidWorks Automation

This macro is contextualized with the three quiz images and the supplied helical-gear PDFs.

## Quiz 1 — theory
Prompts for `Z1`, `Z2`, `M`, `Alfa`, and helical angle, then writes the main equations into SolidWorks Equation Manager: `Dp`, `De`, `Di`, `Ct`, `P`, `r`, and `Delta`.

## Quiz 2 — gears
Creates two parametric gear-part bases using the assigned `Z1` and `Z2`, and saves names in the required pattern:

`N#_Q#_M#_A#`

The PDF-specific tooth arc table (`R1`, `R2`, `R3`), swept cut, circular pattern, and functional assembly still require SolidWorks topology selections and must be completed/validated in SolidWorks. The macro intentionally does not fake those selections.

## Quiz 3 — threaded union
Calculates the thread pitch from threads per inch:

`pitch_mm = (1 / TPI) * 25.4`

It records the five required components as the next modeling checklist. Student-specific UNC/UNF dimensions from the image must be entered from the assigned row.

## Testing
Run `main`, select each quiz, and test these rows from the provided table:

- `STUDENT C`: Z1 38, Z2 19, M 2, Alfa 20°, helix 25°.
- `STUDENT D`: Z1 36, Z2 18, M 2, Alfa 20°, helix 5°.
- `STUDENT E`: Z1 24, Z2 48, M 3, Alfa 15°, helix 10°.

SolidWorks runtime validation is required; it cannot be performed in this environment.
