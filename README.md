# Re-entry Vehicle Aero-Thermal Analysis

Coupled aerodynamic and thermal analysis of a Dragon-style blunt-body capsule during
atmospheric re-entry. CFD surface pressure validated against analytical theory across a
Mach sweep, coupled to a transient thermal protection system (TPS) model over a
representative LEO return trajectory.

**Tools:** ANSYS SpaceClaim · ANSYS Meshing · ANSYS Fluent 2026 R1 (Student) · Python 3

---

## Headline results

**CFD validated to within 3% of analytical theory across three Mach numbers.**

| Mach | Peak wall static pressure | vs Rayleigh Pitot | Peak C_p | vs Newtonian | Freestream P₀ | vs isentropic |
|---|---|---|---|---|---|---|
| 5.0 | 9,262 Pa | 1.22 % | 1.786 | 1.26 % | 152,514 Pa | 0.39 % |
| 7.5 | 11,173 Pa | 2.81 % | 1.878 | 2.85 % | 966,595 Pa | 0.76 % |
| 10.0 | 10,249 Pa | 0.58 % | 1.821 | 0.59 % | 3,421,984 Pa | 1.07 % |

**TPS sizing** — thickness required to hold bondline below 523 K over the entry:

| Material | Thickness | Peak surface T | Peak bondline T | Areal mass |
|---|---|---|---|---|
| PICA | 4.0 cm | 2,203 K | 458 K | 10.8 kg/m² |
| Avcoat | 3.0 cm | 2,200 K | 462 K | 15.4 kg/m² |
| Generic ablator | 3.5 cm | 1,700 K | 455 K | 9.2 kg/m² |

Integrated heat load ≈ 62 MJ/m². Peak Mach 27.7, 354 s from entry interface to 20 km.

---

## Repository layout

```
├── docs/
│   └── PROJECT_STATUS.md      full technical record: setup, results, limitations
├── scripts/
│   ├── mesh_independence.py   grid convergence study
│   ├── validation_chart.py    CFD vs analytical theory, 3-panel
│   ├── cp_comparison.py       C_p distribution across three Mach numbers
│   ├── fay_riddell.py         stagnation heating, Mach 5–25, vs Sutton-Graves
│   └── tps_thermal.py         trajectory + 1-D transient TPS conduction
├── results/
│   ├── week1/                 mesh independence
│   ├── week2/                 CFD validation, C_p distributions and raw exports
│   ├── week4/                 heating profiles and TPS thermal response
│   └── screenshots/           ANSYS captures
```

## Reproducing

```bash
pip install numpy matplotlib
cd scripts
python mesh_independence.py
python validation_chart.py
python cp_comparison.py
python fay_riddell.py
python tps_thermal.py
```

ANSYS case files are not committed — they exceed practical repository size. Setup is fully
documented in `docs/PROJECT_STATUS.md` sections 2–5 and can be rebuilt from a STEP import.

---

## Method

1. **Geometry** — STEP import; spherical far-field domain (≈20 × body diameter) generated
   with the SpaceClaim Enclosure tool. Nose radius fitted from surface points: R_n = 3.248 m.
2. **Mesh** — 479,475 cells, sized against the 512k ANSYS Student cap. Grid convergence
   established at Mach 5.
3. **CFD** — density-based, k-ω SST, ideal gas, Sutherland viscosity, Roe-FDS, isothermal
   300 K wall. Mach 5 / 7.5 / 10, ramped between cases from converged solutions.
4. **Validation** — peak wall static pressure vs Rayleigh Pitot, peak C_p vs modified
   Newtonian, freestream P₀ vs isentropic.
5. **Heating** — Fay-Riddell stagnation-point convective heating, cross-checked against
   Sutton-Graves (agreement to 0.3 % at Mach 10).
6. **Trajectory** — Allen-Eggers ballistic entry solution, β = 667 kg/m², γ = −5.5°.
7. **TPS** — 1-D transient conduction, implicit scheme, reradiating and ablating front face,
   adiabatic back face. Thickness sized to a bondline limit.

## Limitations

Documented in full in `docs/PROJECT_STATUS.md` section 8. In brief: no inflation layers
(so CFD wall heat flux is not used — heating is computed analytically); Mach 15 did not
converge on the available mesh; calorically perfect gas throughout, which is invalid above
roughly Mach 12; first-order spatial discretisation; simplified ablation without surface
recession. Sized TPS thicknesses under-predict flight hardware by roughly a factor of two.
