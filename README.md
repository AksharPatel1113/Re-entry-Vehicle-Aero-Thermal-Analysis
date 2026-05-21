# Re-entry-Vehicle-Aero-Thermal-Analysis
# Re-entry Vehicle Aero-Thermal Analysis
**Dragon-style blunt body capsule | Mach 5–25 | ANSYS Fluent + Thermal**

## Project Overview
Coupled aerodynamic and thermal analysis of a blunt-body capsule during atmospheric
re-entry. Phase 1: CFD pressure/heat flux distributions. Phase 2: Transient TPS thermal model.

## Structure
```
├── geometry/          # SpaceClaim .scdoc files
├── mesh/              # ANSYS Meshing files (.msh)
├── cfd/
│   ├── week1_euler/   # Inviscid baseline runs
│   ├── week2_viscous/ # k-ω SST & Spalart-Allmaras
│   └── week3_heat_flux/ # Energy equation, heat flux extraction
├── thermal/           # ANSYS Thermal TPS model
├── scripts/           # Python automation scripts
├── results/           # Plots, data, screenshots
└── report/            # LaTeX technical report
```

## Key Results
| Case | Mach | Stag. Pressure (CFD) | Theory | Error |
|------|------|----------------------|--------|-------|
| Baseline | 5 | 147,135 Pa | 151,849 Pa | 2.4% |

## Mesh Independence Study
| Mesh | Cells | Stag. Pressure |
|------|-------|----------------|
| Coarse | 272k | diverged |
| Medium | 358k | 74,900 Pa |
| Fine   | 479k | 147,135 Pa ✓ |

Fine mesh selected for all production runs (2.4% error vs isentropic theory).

## Software
- ANSYS SpaceClaim 2026 R1
- ANSYS Meshing 2026 R1
- ANSYS Fluent 2026 R1 (Student)
- Python 3.x (matplotlib, numpy)
- LaTeX / Overleaf
