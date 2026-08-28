"""
Mesh independence study — Dragon capsule re-entry CFD
Mach 5, ~40 km, inviscid (Euler), ANSYS Fluent 2026 R1 Student
"""
import numpy as np, matplotlib.pyplot as plt, matplotlib.ticker as tk

g, M, P_inf = 1.4, 5.0, 287.14
P0 = P_inf*(1+(g-1)/2*M**2)**(g/(g-1))

cells = [272_000, 358_000, 479_337]
stag  = [None,     74_900,  147_135]        # Pa, coarse mesh diverged

print(f"Isentropic P0 : {P0:.1f} Pa")
print(f"Fine mesh     : {stag[2]:,} Pa  ({abs(P0-stag[2])/P0*100:.2f}% error)")

fig, ax = plt.subplots(figsize=(9,6))
fig.patch.set_facecolor('#FAFAFA'); ax.set_facecolor('#FAFAFA')

ax.plot(cells[1:], stag[1:], 'o-', color='#185FA5', lw=2.5, ms=10,
        mfc='white', mew=2.5, label='CFD (Euler, Mach 5)', zorder=4)
ax.plot(cells[0], 38_000, 'x', color='#D85A30', ms=13, mew=2.5,
        label='Coarse mesh (diverged, excluded)', zorder=4)
ax.axhline(P0, color='#1D9E75', ls='--', lw=1.8, label=f'Isentropic theory: {P0:.0f} Pa')
ax.axhspan(P0*0.95, P0*1.05, alpha=0.10, color='#1D9E75', label='±5% band')

ax.annotate('Diverged\n(coarse-grid instability)', xy=(cells[0],38_000),
            xytext=(200_000,62_000), fontsize=8, color='#D85A30',
            arrowprops=dict(arrowstyle='->', color='#D85A30', lw=1.2))
ax.annotate(f'Δ = {abs(P0-147_135)/P0*100:.1f}% vs theory\n→ mesh independent',
            xy=(cells[2],147_135), xytext=(400_000,168_000), fontsize=9,
            color='#1D9E75', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#1D9E75', lw=1.2))

ax.set_xlabel('Mesh cell count', fontsize=12)
ax.set_ylabel('Stagnation-point total pressure [Pa]', fontsize=12)
ax.set_title('Mesh independence study — Dragon capsule re-entry\n'
             'Mach 5 · 40 km · Euler · ANSYS Fluent 2026 R1', fontsize=12, pad=12)
ax.set_xlim(180_000,560_000); ax.set_ylim(0, P0*1.4)
ax.xaxis.set_major_formatter(tk.FuncFormatter(lambda x,_: f'{int(x/1000)}k'))
ax.yaxis.set_major_formatter(tk.FuncFormatter(lambda y,_: f'{y:,.0f}'))

ax2 = ax.twiny(); ax2.set_xlim(ax.get_xlim()); ax2.set_xticks(cells)
ax2.set_xticklabels(['Coarse\n(272k)','Medium\n(358k)','Fine\n(479k)'], fontsize=9)
ax2.spines['top'].set_linewidth(0.5)

ax.legend(fontsize=9, loc='upper left'); ax.grid(ls='--', alpha=0.4, lw=0.5)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('../results/week1/mesh_independence_plot.png', dpi=150,
            bbox_inches='tight', facecolor='#FAFAFA')
