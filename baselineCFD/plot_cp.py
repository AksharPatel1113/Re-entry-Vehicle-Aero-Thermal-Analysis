"""
Cp Distribution Plot — Dragon Capsule Re-entry CFD
Mach 5, k-omega SST, ANSYS Fluent 2026 R1
Author: Akshar Patel | Date: May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import re

def read_fluent_xy(filepath):
    """Read Fluent XY plot export file → returns (x, cp) arrays sorted by x."""
    x_vals, cp_vals = [], []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip header lines
            if line.startswith('(') or line.startswith(')') or not line:
                continue
            parts = line.split()
            if len(parts) == 2:
                try:
                    x_vals.append(float(parts[0]))
                    cp_vals.append(float(parts[1]))
                except ValueError:
                    continue
    x = np.array(x_vals)
    cp = np.array(cp_vals)
    # Sort by x position
    idx = np.argsort(x)
    return x[idx], cp[idx]

# ── Read data ─────────────────────────────────────────────────────────────────
x, cp = read_fluent_xy('/home/claude/reentry_project/week1/cp_mach5_komega.xy')

print(f"Data points loaded : {len(x)}")
print(f"X range            : {x.min():.3f} to {x.max():.3f} m")
print(f"Cp range           : {cp.min():.4f} to {cp.max():.4f}")
print(f"Max Cp (stag pt)   : {cp.max():.4f} at x = {x[np.argmax(cp)]:.3f} m")

# ── Theoretical Cp at stagnation (isentropic, Mach 5) ─────────────────────────
gamma = 1.4
M = 5.0
# Cp_max = 2/(gamma*M^2) * [(P0/P_inf) - 1]
P0_ratio = (1 + (gamma-1)/2 * M**2)**(gamma/(gamma-1))
Cp_theory_stag = 2/(gamma * M**2) * (P0_ratio - 1)
print(f"Theoretical Cp stag: {Cp_theory_stag:.4f}")

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
fig.patch.set_facecolor('#FAFAFA')

# ── Left plot: full Cp distribution ──────────────────────────────────────────
ax1.set_facecolor('#FAFAFA')
ax1.scatter(x, cp, s=1.5, color='#185FA5', alpha=0.4, label='CFD data points')

# Rolling mean for clean line
window = 80
cp_smooth = np.convolve(cp, np.ones(window)/window, mode='valid')
x_smooth  = x[window//2 : window//2 + len(cp_smooth)]
ax1.plot(x_smooth, cp_smooth, color='#185FA5', linewidth=2,
         label='Smoothed Cp', zorder=3)

# Theory stagnation line
ax1.axhline(y=Cp_theory_stag, color='#1D9E75', linewidth=1.5,
            linestyle='--', label=f'Theory Cp_stag = {Cp_theory_stag:.3f}')

ax1.set_xlabel('X Position [m]', fontsize=11)
ax1.set_ylabel('Pressure Coefficient Cp', fontsize=11)
ax1.set_title('Cp Distribution — Full Capsule Surface\n'
              'Mach 5 · k-ω SST · ANSYS Fluent 2026 R1', fontsize=11)
ax1.legend(fontsize=9, framealpha=0.9)
ax1.grid(True, linestyle='--', alpha=0.4, linewidth=0.5)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ── Right plot: nose region zoom (stagnation point) ──────────────────────────
ax2.set_facecolor('#FAFAFA')

# Focus on nose region (positive x, forward hemisphere)
nose_mask = (x > 0.5) & (x < 1.3)
ax2.scatter(x[nose_mask], cp[nose_mask], s=3, color='#185FA5',
            alpha=0.5, label='CFD data points')

# Smooth for nose region
if nose_mask.sum() > window:
    x_n  = x[nose_mask]
    cp_n = cp[nose_mask]
    cp_ns = np.convolve(cp_n, np.ones(40)/40, mode='valid')
    x_ns  = x_n[20:20+len(cp_ns)]
    ax2.plot(x_ns, cp_ns, color='#185FA5', linewidth=2, label='Smoothed Cp')

ax2.axhline(y=Cp_theory_stag, color='#1D9E75', linewidth=1.5,
            linestyle='--', label=f'Theory Cp_stag = {Cp_theory_stag:.3f}')

# Mark max Cp point
max_idx = np.argmax(cp[nose_mask])
x_nose = x[nose_mask]
cp_nose = cp[nose_mask]
ax2.plot(x_nose[max_idx], cp_nose[max_idx], 'o', color='#D85A30',
         markersize=8, markerfacecolor='white', markeredgewidth=2,
         label=f'Max Cp = {cp_nose[max_idx]:.3f}', zorder=5)

ax2.set_xlabel('X Position [m]', fontsize=11)
ax2.set_ylabel('Pressure Coefficient Cp', fontsize=11)
ax2.set_title('Cp Distribution — Nose/Stagnation Region\n'
              'Mach 5 · k-ω SST · ANSYS Fluent 2026 R1', fontsize=11)
ax2.legend(fontsize=9, framealpha=0.9)
ax2.grid(True, linestyle='--', alpha=0.4, linewidth=0.5)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/home/claude/reentry_project/week1/cp_mach5_komega_plot.png',
            dpi=150, bbox_inches='tight', facecolor='#FAFAFA')
print("Saved cp_mach5_komega_plot.png")
plt.close()
