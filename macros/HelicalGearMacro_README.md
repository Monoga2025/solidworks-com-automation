# SolidWorks helical gear macro

## Context
The ZIP chat was used to identify the assignment context. The actual modeling specification is in `Manual_Maestro_Engranajes_Helicoidales_SolidWorks.pdf` and `Tutorial_Modelado_Engranajes_Helicoidales_SolidWorks.pdf`: a parametric helical gear exercise for 25 and 33 teeth.

## Run
1. Open SolidWorks (2019 or newer recommended).
2. Open **Tools > Macro > New**, save a `.swp`, or import `HelicalGearMacro.bas` into the VBA editor.
3. Set the constants at the top of the module. Use `TEETH = 25` for gear 1 or `TEETH = 33` for gear 2.
4. Run `main`.
5. Inspect the created part and the Equation Manager.

## What it automates
- New part creation.
- Global equations for module, tooth count, pitch diameter, outside/root references, face width, chamfer and bore.
- Cylindrical gear blank.
- Bore and keyway cuts.
- Reference circles and a reference line for the helix workflow.

## Important limitation
The PDFs rely on manually selected tooth-profile arcs, a reference plane, a 30-degree helix, and a swept/lofted cut. Those selections are topology-dependent and vary across SolidWorks versions. This macro deliberately stops after creating named reference geometry instead of producing a potentially incorrect tooth profile. Finish the profile and circular pattern following the PDF's audited frames. A SolidWorks runtime test is still required.
