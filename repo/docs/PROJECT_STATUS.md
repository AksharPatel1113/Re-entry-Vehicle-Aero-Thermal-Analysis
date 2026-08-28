# Re-entry Vehicle Aero-Thermal Analysis — Project Status

**Vehicle:** Dragon-style blunt-body capsule, 3.6 m diameter
**Software:** ANSYS SpaceClaim / Meshing / Fluent 2026 R1 Student Edition, Python 3
**Status:** Complete — Weeks 1–4

---

## 1. Executive summary

A coupled aero-thermal analysis of a blunt-body re-entry capsule. Phase 1 (CFD) produces
surface pressure and Cp distributions across a Mach sweep, validated against normal-shock
and Newtonian theory. Phase 2 (thermal) couples stagnation heating into a transient TPS model.

**Three CFD cases converged and validated to within 3% of analytical theory.** Stagnation
heating computed analytically across Mach 5–25 via Fay-Riddell, cross-checked against
Sutton-Graves, and anchored to the CFD-validated range.

---

## 2. Geometry

| Parameter | Value | Note |
|---|---|---|
| Capsule diameter | 3.6 m | |
| Fitted nose radius R_n | **3.248 m** | least-squares spherical-cap fit to CFD surface points |
| Heat-shield orientation | normal to −Y | capsule body extends toward +Y |
| Freestream direction | **+Y** (0, 1, 0) | flow impinges on heat shield |
| Domain shape | sphere | generated via SpaceClaim **Enclosure** tool |
| Domain cushion | 700 % | |
| Domain radius | ≈ 35.6 m | ≈ 20 × body diameter |
| Fluid volume | 1.893 × 10¹⁴ mm³ | |

### Import path
SLDPRT import failed. **STEP** import succeeded and preserved solid topology, avoiding
facet-to-solid conversion entirely.

### Domain creation
Manual Boolean subtract failed repeatedly — root cause was the imported capsule sitting
off-origin, so the sphere and capsule never intersected and `Combine` returned the target
unchanged with no error. The **Enclosure** tool (Prepare → Analysis) creates the domain and
subtracts the body in one operation regardless of body position, and resolved this.

### Named selections
- `pressure_far_field` — outer sphere surface
- `wall_capsule` → appears in Fluent as `wall-enclosure_enclosure`

Assigned in SpaceClaim via Groups → Create NS. Selecting inner faces used
Selection → Features → **Inner faces**, which captures all capsule surfaces in one action.

---

## 3. Mesh

| Setting | Value |
|---|---|
| Physics / Solver preference | CFD / Fluent |
| Element size | 6.5 m |
| Max size | 8.5 m |
| Capture curvature | Yes |
| Curvature normal angle | 10° |
| **Cell count** | **479,475** |
| Inflation layers | none (see limitations) |

### Mesh independence study (earlier domain configuration)

| Level | Element size | Cells |
|---|---|---|
| Coarse | 7 m | 272,000 |
| Medium | 5 m | 358,000 |
| Fine | 3.5 m | 479,337 |

Constrained by the ANSYS Student **512,000 cell cap**. Element size was tuned iteratively
(3.5 → 6.5 m) after the domain was enlarged to 20× diameter, since the larger domain at
constant element size exceeded the cap (949,913 cells at 4 m).

---

## 4. Solver configuration

| Setting | Value |
|---|---|
| Solver type | Density-based, steady, absolute velocity |
| Turbulence model | k-ω SST |
| Energy equation | On |
| Density | Ideal gas |
| Viscosity | Sutherland (3-coefficient) |
| Wall BC | No-slip, isothermal **300 K** |
| Operating pressure | 0 Pa |
| Flux type | Roe-FDS |
| Spatial discretisation | First Order Upwind (flow, TKE, SDR) |
| Initialisation | **Hybrid** |
| Residual criteria | 1 × 10⁻⁴ |

**Courant number by case:** Mach 5 → 0.5 · Mach 7.5 → 0.3 · Mach 10 → 0.2 (ramped)

Second-order upwind was attempted and caused divergence. First order retained throughout;
see limitations.

---

## 5. Freestream conditions

| Case | Alt (km) | Mach | P∞ (Pa) | T∞ (K) | ρ∞ (kg/m³) | V∞ (m/s) | q∞ (Pa) |
|---|---|---|---|---|---|---|---|
| 1 | 40 | 5.0 | 287.14 | 250.35 | 3.996 × 10⁻³ | 1586 | 5025 |
| 2 | 45 | 7.5 | 149.10 | 264.16 | 1.966 × 10⁻³ | 2444 | 5871 |
| 3 | 50 | 10.0 | 79.78 | 270.65 | 1.027 × 10⁻³ | 3298 | 5585 |
| — | 60 | 15.0 | 21.96 | 247.02 | 3.097 × 10⁻⁴ | 4726 | 3459 |
| — | 70 | 20.0 | 5.221 | 219.59 | 8.283 × 10⁻⁵ | 5941 | 1462 |
| — | 75 | 25.0 | 2.388 | 208.40 | 3.992 × 10⁻⁵ | 7235 | 1045 |

Turbulence BC for all cases: intensity 1 %, viscosity ratio 10.

---

## 6. CFD results — validation against theory

### Peak wall static pressure vs Rayleigh Pitot

| Mach | CFD (Pa) | Theory (Pa) | Error |
|---|---|---|---|
| 5.0 | 9,262.0 | 9,376.1 | **1.22 %** |
| 7.5 | 11,172.6 | 10,867.5 | **2.81 %** |
| 10.0 | 10,248.8 | 10,308.9 | **0.58 %** |

### Peak Cp vs modified Newtonian

| Mach | CFD | Theory | Error |
|---|---|---|---|
| 5.0 | 1.786 | 1.809 | 1.26 % |
| 7.5 | 1.878 | 1.826 | 2.85 % |
| 10.0 | 1.821 | 1.832 | 0.59 % |

### Freestream total pressure vs isentropic (BC validation)

| Mach | CFD (Pa) | Theory (Pa) | Error |
|---|---|---|---|
| 5.0 | 152,514 | 151,923 | 0.39 % |
| 7.5 | 966,595 | 959,299 | 0.76 % |
| 10.0 | 3,421,984 | 3,385,802 | 1.07 % |

### Observations
- Cp on the heat shield is nearly **Mach-independent** above M≈4 — theory predicts 1.809 at
  M5 and 1.832 at M10, under 2 % apart across a doubling of speed. CFD reproduces this.
- Mach 7.5 Cp (1.878) slightly **exceeds** the Newtonian bound of 1.826. Attributed to
  single-facet pressure spike from shock smearing on a coarse grid. Area-weighted averaging
  recommended as a cross-check.
- Total pressure loss across the bow shock at Mach 5: freestream P₀ 152,514 Pa →
  wall 9,262 Pa, a **93.9 % loss**, consistent with strong normal-shock behaviour.

---

## 7. Analytical heating — Fay-Riddell

Implemented per Fay & Riddell (1958), equilibrium boundary layer:

```
q_w = 0.763 · Pr^(−0.6) · (ρ_e μ_e)^0.4 · (ρ_w μ_w)^0.1 · √(du_e/dx) · (h_0e − h_w)
du_e/dx = (1/R_n) · √(2(P_e − P∞)/ρ_e)
```

R_n = 3.248 m (fitted from CFD geometry), T_w = 300 K, Sutherland viscosity.

| Mach | Alt (km) | V (m/s) | T₀ (K) | q Fay-Riddell | q Sutton-Graves | Δ |
|---|---|---|---|---|---|---|
| 5.0 | 40 | 1586 | 1,502 | 2.15 W/cm² | 2.44 W/cm² | 11.8 % |
| 7.5 | 45 | 2444 | 3,236 | 5.98 | 6.25 | 4.3 % |
| 10.0 | 50 | 3298 | 5,684 | 11.07 | 11.11 | **0.3 %** |
| 15.0 | 60 | 4726 | 11,363 | 18.61 | 17.95 | 3.7 % |
| 20.0 | 70 | 5941 | 17,787 | 19.59 | 18.44 | 6.2 % |
| 25.0 | 75 | 7235 | 26,258 | 25.09 | 23.12 | 8.5 % |

Two independent correlations agreeing to 0.3 % at Mach 10 validates the implementation.

**Methodology note.** CFD is validated against theory over Mach 5–10, where the mesh
resolves the shock adequately. Fay-Riddell — validated in that range — is then used to
generate heating at Mach 15–25 for the TPS analysis. This mirrors preliminary-design
practice: anchor a cheap correlation to high-fidelity data where high-fidelity is
affordable, then extrapolate with the correlation.

---

## 7A. Entry trajectory

Allen-Eggers ballistic solution, exponential atmosphere (ρ₀ = 1.225 kg/m³, H = 7,200 m).

| Parameter | Value |
|---|---|
| Entry velocity | 7,600 m/s |
| Flight path angle | −5.5° |
| Vehicle mass | 9,500 kg (representative) |
| Drag coefficient | 1.4 |
| Reference area | 10.18 m² |
| **Ballistic coefficient β** | **667 kg/m²** |
| Peak Mach | 27.7 |
| Duration, entry interface to 20 km | 354 s |

Fay-Riddell evaluated continuously along this trajectory gives the heat-flux history that
drives the thermal model, rather than the discrete Mach points of section 7.

---

## 7B. Transient TPS thermal analysis

### Model
1-D transient conduction through the TPS thickness, implicit (backward Euler), 120 nodes.

- **Front face:** q_net = q_conv − εσ(T⁴ − T∞⁴), with surface temperature capped at the
  material ablation temperature and excess flux booked as absorbed by ablation
- **Back face:** adiabatic (conservative — no heat rejection to structure)
- **Sizing criterion:** peak bondline temperature below 523 K (250 °C)

### Material properties (representative open-literature values)

| Material | ρ (kg/m³) | k (W/m·K) | c_p (J/kg·K) | T_abl (K) | ε |
|---|---|---|---|---|---|
| PICA | 270 | 0.35 | 1,590 | 2,900 | 0.90 |
| Avcoat | 512 | 0.35 | 1,465 | 2,200 | 0.85 |
| Generic ablator | 264 | 0.213 | 1,255 | 1,700 | 0.85 |

Properties should be verified against primary sources before publication.

### Results

| Material | Sized thickness | Peak surface T | Peak bondline T | Areal mass | Integrated load |
|---|---|---|---|---|---|
| PICA | 4.0 cm | 2,203 K | 458 K | **10.8 kg/m²** | 61.6 MJ/m² |
| Avcoat | 3.0 cm | 2,200 K | 462 K | 15.4 kg/m² | 61.5 MJ/m² |
| Generic ablator | 3.5 cm | 1,700 K | 455 K | 9.2 kg/m² | 63.0 MJ/m² |

### Discussion
Avcoat requires less thickness than PICA because its lower ablation temperature caps surface
temperature sooner, reducing the gradient driving heat inward. At 512 kg/m³ it nevertheless
carries a **43 % areal-mass penalty** relative to PICA — the reason low-density ablators
displaced Avcoat-class materials on modern vehicles.

The generic silicone ablator shows the lowest areal mass, but its 1,700 K ablation limit
means it would recede fastest in service. The model does not track surface recession, so
this comparison understates its true thickness requirement.

### Model limitations
- Ablation is a temperature cap with energy bookkeeping, not a mass-loss-coupled model
- **No surface recession**
- Constant properties — no temperature dependence, pyrolysis, or char-layer formation
- Radiative heating omitted (defensible at 7.6 km/s, not negligible)
- Stagnation point only; the remainder of the heat shield sees lower flux
- No design margins applied

**Sized thicknesses under-predict flight hardware by roughly a factor of two** — actual
PICA-X on Dragon is substantially thicker than the 4.0 cm computed here. The model captures
the correct physics and the correct relative ranking between materials, but should be read
as preliminary sizing, not a design value.

---

## 8. Known limitations

### 8.1 No inflation layers
Inflation generated inverted/failed cells around the capsule across multiple attempts
(First Layer Thickness 0.1 mm × 20 layers; Smooth Transition 0.272 × 5 layers). Root cause
is complex imported surface topology. Consequence: the near-wall boundary layer is
unresolved, so **wall heat flux from CFD is not trustworthy** — this is why heating is
computed analytically rather than extracted from the solver. Surface pressure, which is
driven by the inviscid outer flow, remains valid.

### 8.2 Mach 15 convergence failure
Two attempts:
- **Cold start, Courant 0.25** — residuals idled at 1e-1 for 750 iterations, then diverged
  to 1e+8 at iteration 860. Stagnation pressure monitor read 350 MPa vs 6.4 kPa theory.
- **Courant 0.05** — no blowup, but residuals bottomed at iteration ~350 and climbed
  thereafter. Stagnation pressure settled at 5,510 Pa vs 6,399 Pa theory (14 % low).

Ramping from the converged Mach 5 solution also failed. Cause is mesh resolution: shock
thickness scales inversely with Mach number, so a shock marginally resolved at Mach 5 is
under-resolved at Mach 15. The 512k cell cap prevents the refinement that would fix it.
Mach 15 and 25 are therefore covered analytically.

### 8.3 Perfect-gas assumption
Calorically perfect air (γ = 1.4) throughout. Above ≈ Mach 12, O₂ and N₂ dissociation
becomes significant and effective γ falls well below 1.4. Perfect-gas theory predicts
T₀ = 26,258 K at Mach 25; real shock-layer temperature would be roughly 8,000–10,000 K,
with the balance absorbed by dissociation. **CFD results above Mach 12 were not attempted
for this reason.** Fay-Riddell is the more appropriate tool there, as it carries Lewis
number and dissociation enthalpy terms explicitly.

### 8.4 First-order discretisation
Second-order upwind destabilised the solution (residual spike at iteration 3000 on the
Mach 5 case). First order retained. Expected consequence is additional numerical diffusion
and a slightly smeared shock.

---

## 9. Debugging log — errors found and corrected

| # | Issue | Detection | Resolution |
|---|---|---|---|
| 1 | Vehicle flying nose-first instead of heat-shield-first | Reviewed expected stagnation location against geometry | Flow direction vector set to (0, 1, 0) |
| 2 | Reference Values left at solver defaults (ρ=1.225, V=1) | Exported Cp read 77–15,121 vs physical max ≈1.8 | Compute-from set to far-field zone; earlier data rescaled analytically |
| 3 | Boolean subtract silently no-op | Domain volume matched a bare sphere exactly | Switched to Enclosure tool |
| 4 | Capsule retained as solid cell zone | Cell Zone Conditions showed fluid + solid, shadow walls, contact interfaces | Suppress for Physics on the capsule body |
| 5 | Node-based vs cell-based Cp export | Mach 10 peak Cp read 1.611 vs 1.821 from facet maximum | Cell-centred export specified |
| 6 | Mesh exceeded Student cell cap | 949,913 cells at 4 m element size | Element size tuned to 6.5 m → 479,475 |

Item 1 is the most consequential. Stagnation heat flux scales as 1/√R_n, so flying the
low-radius nose into the flow rather than the large-radius heat shield would have
substantially over-predicted heating and inverted the entire pressure distribution.

---

## 10. Files

### Generated analysis
| File | Contents |
|---|---|
| `validation_mach_sweep.png` | 3-panel: wall pressure, Cp, freestream P₀ vs theory |
| `cp_mach5_corrected.png` | Mach 5 Cp distribution + Newtonian comparison |
| `cp_comparison_m5_m10.png` | Two-Mach Cp distribution comparison |
| `fay_riddell_heating.png` | Heating and T₀ vs Mach, 5–25 |
| `mesh_independence_plot.png` | Stagnation pressure vs cell count |
| `fay_riddell_results.csv` | Tabulated heating data |
| `cp_mach5_corrected.csv` | Rescaled Mach 5 surface data |

### Scripts
`mesh_independence.py` · `plot_cp.py` · `val.py` (validation chart) · `fr.py` (Fay-Riddell)

### ANSYS cases
`mach5_komega_corrected` · `mach7p5_komega` · `mach10_komega` (.cas.h5 / .dat.h5)

### Screenshots to file into `results/screenshots/`
| Screenshot | Shows |
|---|---|
| SpaceClaim structure tree + sphere | Domain creation |
| ANSYS Meshing details panel | Mesh settings, 479,475 elements |
| Mesh section plane through capsule | Interior mesh, capsule void |
| Failed inflation layers (magenta cells) | Limitation 8.1 evidence |
| Mach 5 residual history | Convergence to 1e-3 |
| Mach 5 static pressure contour on wall | **Orientation verification** — peak on heat shield |
| Mach 15 divergence (1e+8 residuals) | Limitation 8.2 evidence |
| Mach 15 stagnation monitor at 350 MPa | Limitation 8.2 evidence |
| Mach 10 ramped residual history | BC change at iteration 2500, recovery |
| Mach 7.5 residual history | Cleanest convergence of the three |
| Mach 7.5 stagnation pressure monitor | Settled 11,150 Pa from iteration 1400 |

---

## 11. Next steps

### Remaining
1. LaTeX technical report
2. LinkedIn post
3. File ANSYS screenshots into `results/screenshots/` per section 10
4. Verify TPS material properties against primary sources

### Deferred / optional
- Rebuild mesh at 10× domain instead of 20× to recover shock-layer resolution; may open up Mach 15
- Spalart-Allmaras comparison at Mach 5 (original Week 2 scope, not yet run)
- Angle-of-attack sweep 0–10° (requires full 3-D, no axisymmetric shortcut)
