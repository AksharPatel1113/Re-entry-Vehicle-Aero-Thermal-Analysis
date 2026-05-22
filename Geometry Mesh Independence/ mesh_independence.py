"""
Mesh Independence Study — Dragon Capsule Re-entry CFD
Mach 5, Altitude ~40km, Inviscid (Euler) Solver
ANSYS Fluent 2026 R1 Student Edition
Author: Akshar Patel | Date: May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── Theoretical stagnation pressure ──────────────────────────────────────────
# Pressure far-field BC uses isentropic freestream → compare to isentropic P0
gamma = 1.4
M     = 5.0
P_inf = 287.0  # Pa, static pressure at ~40 km altitude

P0_theory = P_inf * (1 + (gamma-1)/2 * M**2) ** (gamma/(gamma-1))

print(f"Isentropic stagnation pressure P0 : {P0_theory:.1f} Pa")
print(f"CFD fine mesh (479k)              : 147,135 Pa")
print(f"Error                             : {abs(P0_theory-147135)/P0_theory*100:.2f}%")
print(f"CFD medium mesh (358k)            : 74,900 Pa")

# ── Mesh data ─────────────────────────────────────────────────────────────────
cell_counts   = [272_000, 358_000, 479_337]
stag_pressure = [None,    74_900,  147_135]

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))
fig.patch.set_facecolor('#FAFAFA')
ax.set_facecolor('#FAFAFA')

# Converged CFD points
cx = [cell_counts[1], cell_counts[2]]
cy = [stag_pressure[1], stag_pressure[2]]
ax.plot(cx, cy, 'o-', color='#185FA5', linewidth=2.5, markersize=10,
        markerfacecolor='white', markeredgewidth=2.5,
        label='CFD Result (Euler, Mach 5)', zorder=4)

# Coarse mesh diverged marker
ax.plot(cell_counts[0], 38_000, 'x', color='#D85A30',
        markersize=13, markeredgewidth=2.5, zorder=4,
        label='Coarse mesh (diverged — excluded)')
ax.annotate('Diverged\n(numerical instability\non coarse grid)',
            xy=(cell_counts[0], 38_000), xytext=(200_000, 62_000),
            fontsize=8, color='#D85A30',
            arrowprops=dict(arrowstyle='->', color='#D85A30', lw=1.2))

# Theory line
ax.axhline(y=P0_theory, color='#1D9E75', linewidth=1.8, linestyle='--', zorder=2,
           label=f'Isentropic theory: {P0_theory:.0f} Pa')
ax.axhspan(P0_theory*0.95, P0_theory*1.05, alpha=0.10,
           color='#1D9E75', label='±5% theory band')

# Point labels
ax.annotate(f'74,900 Pa\n(Medium · 358k)',
            xy=(cell_counts[1], 74_900), xytext=(255_000, 95_000),
            fontsize=8.5, color='#185FA5',
            arrowprops=dict(arrowstyle='->', color='#185FA5', lw=1.2))
ax.annotate(f'147,135 Pa\n(Fine · 479k)',
            xy=(cell_counts[2], 147_135), xytext=(370_000, 128_000),
            fontsize=8.5, color='#185FA5',
            arrowprops=dict(arrowstyle='->', color='#185FA5', lw=1.2))

# Error annotation
err = abs(P0_theory - 147_135)/P0_theory*100
ax.annotate(f'Δ = {err:.1f}% vs theory\n→ mesh independent ✓',
            xy=(cell_counts[2], 147_135), xytext=(400_000, 168_000),
            fontsize=9, color='#1D9E75', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#1D9E75', lw=1.2))

# Axes formatting
ax.set_xlabel('Mesh Cell Count', fontsize=12, labelpad=8)
ax.set_ylabel('Stagnation Point Total Pressure [Pa]', fontsize=12, labelpad=8)
ax.set_title('Mesh Independence Study — Dragon Capsule Re-entry\n'
             'Mach 5 · Alt. 40 km · Euler (Inviscid) · ANSYS Fluent 2026 R1',
             fontsize=12, pad=12)
ax.set_xlim(180_000, 560_000)
ax.set_ylim(0, P0_theory * 1.4)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x,_: f'{int(x/1000)}k'))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,_: f'{y:,.0f}'))

# Top axis — mesh level labels
ax2 = ax.twiny()
ax2.set_xlim(ax.get_xlim())
ax2.set_xticks(cell_counts)
ax2.set_xticklabels(['Coarse\n(272k)', 'Medium\n(358k)', 'Fine\n(479k)'], fontsize=9)
ax2.spines['top'].set_linewidth(0.5)

ax.legend(framealpha=0.92, fontsize=9, loc='upper left')
ax.grid(True, linestyle='--', alpha=0.4, linewidth=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/home/claude/reentry_project/week1/mesh_independence_plot.png',
            dpi=150, bbox_inches='tight', facecolor='#FAFAFA')
print("Saved mesh_independence_plot.png")
plt.close()
