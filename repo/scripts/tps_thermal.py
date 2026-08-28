"""
Transient TPS thermal analysis — Dragon-style capsule LEO return
Trajectory: Allen-Eggers ballistic solution
Heating:    Fay-Riddell stagnation-point convective
Conduction: 1-D transient, implicit (backward Euler), reradiating + ablating surface
"""
import numpy as np, matplotlib.pyplot as plt

g,Rgas,Pr,cp_air,sig = 1.4, 287.058, 0.71, 1004.5, 5.670e-8
def mu_s(T): return 1.458e-6*T**1.5/(T+110.4)

# ---------- atmosphere (exponential fit, US Std 1976) ----------
rho0,H = 1.225, 7200.0
def rho_a(h): return rho0*np.exp(-h/H)
def T_a(h):   return np.interp(h,[0,11e3,20e3,32e3,47e3,51e3,71e3,84e3],
                                 [288.15,216.65,216.65,228.65,270.65,270.65,214.65,186.95])

# ---------- vehicle ----------
D, Rn   = 3.6, 3.248            # m  (Rn fitted from CFD geometry)
mass    = 9500.0                # kg  representative Dragon return mass
Cd      = 1.4
A       = np.pi*(D/2)**2
beta    = mass/(Cd*A)           # ballistic coefficient
print(f"Ballistic coefficient beta = {beta:.1f} kg/m^2\n")

# ---------- Allen-Eggers entry ----------
Ve, gam = 7600.0, np.radians(5.5)
h  = np.linspace(120e3, 20e3, 4000)
V  = Ve*np.exp(-rho_a(h)*H/(2*beta*np.sin(gam)))
dt = np.abs(np.diff(h))/(V[:-1]*np.sin(gam)); t = np.concatenate([[0],np.cumsum(dt)])

# ---------- Fay-Riddell along trajectory ----------
def q_fr(V,h,Tw):
    rinf,Tinf = rho_a(h), T_a(h)
    a = np.sqrt(g*Rgas*Tinf); M = V/a
    if M < 1.2: return 0.0
    Pinf = rinf*Rgas*Tinf
    A_=((g+1)**2*M**2)/(4*g*M**2-2*(g-1)); B_=(1-g+2*g*M**2)/(g+1)
    Pe = Pinf*A_**(g/(g-1))*B_
    T0 = Tinf*(1+(g-1)/2*M**2)
    re,me = Pe/(Rgas*T0), mu_s(T0)
    rw,mw = Pe/(Rgas*Tw), mu_s(Tw)
    dudx  = (1/Rn)*np.sqrt(2*(Pe-Pinf)/re)
    return 0.763*Pr**-0.6*(re*me)**0.4*(rw*mw)**0.1*np.sqrt(dudx)*cp_air*(T0-Tw)

M_traj = V/np.sqrt(g*Rgas*T_a(h))
print(f"Peak Mach {M_traj.max():.1f} | entry duration to 20 km: {t[-1]:.0f} s\n")

# ---------- materials (representative open-literature values) ----------
MAT = {
 'PICA':            dict(rho=270., k=0.35, cp=1590., Tabl=2900., eps=0.90, c='#185FA5'),
 'Avcoat':          dict(rho=512., k=0.35, cp=1465., Tabl=2200., eps=0.85, c='#D85A30'),
 'Generic ablator': dict(rho=264., k=0.213,cp=1255., Tabl=1700., eps=0.85, c='#1D9E75')}

def solve(m, L, N=120, Tinit=290., Tback_lim=None):
    """1-D implicit conduction, reradiating+ablating front face, adiabatic back."""
    dx=L/(N-1); T=np.full(N,Tinit); al=m['k']/(m['rho']*m['cp'])
    Ts,Tb,qh,abl = [],[],[],0.0
    for i in range(len(t)-1):
        dtl=t[i+1]-t[i]
        q = q_fr(V[i],h[i],min(T[0],m['Tabl']))
        qr = m['eps']*sig*(T[0]**4-290.**4)
        qn = q-qr
        if T[0]>=m['Tabl']:                 # steady-state ablation cap
            abl += max(qn,0)*dtl; qn=min(qn,0)
        r=al*dtl/dx**2
        Amat=np.zeros((N,N)); b=T.copy()
        Amat[0,0]=1+2*r; Amat[0,1]=-2*r; b[0]=T[0]+2*r*dx*qn/m['k']
        for j in range(1,N-1):
            Amat[j,j-1]=-r; Amat[j,j]=1+2*r; Amat[j,j+1]=-r
        Amat[-1,-1]=1+2*r; Amat[-1,-2]=-2*r
        T=np.linalg.solve(Amat,b)
        T=np.minimum(T,m['Tabl'])
        Ts.append(T[0]); Tb.append(T[-1]); qh.append(q)
    return np.array(Ts),np.array(Tb),np.array(qh),T,abl

# ---------- thickness sizing: bondline < 523 K (250 C) ----------
print(f"{'Material':<17}{'t (cm)':>8}{'T_surf max':>12}{'T_bond max':>12}{'q_int MJ/m2':>13}")
print("-"*62)
sized={}
for nm,m in MAT.items():
    for L in np.arange(0.01,0.121,0.005):
        Ts,Tb,qh,Tp,ab=solve(m,L)
        if Tb.max()<523: break
    Q=np.trapezoid(qh,t[:-1])/1e6
    sized[nm]=(L,Ts,Tb,qh,Tp)
    print(f"{nm:<17}{L*100:>8.1f}{Ts.max():>12.0f}{Tb.max():>12.0f}{Q:>13.1f}")

# ---------- plots ----------
f,ax=plt.subplots(2,2,figsize=(14,9.5)); f.patch.set_facecolor('#FAFAFA')
for a in ax.ravel():
    a.set_facecolor('#FAFAFA'); a.grid(ls='--',alpha=.35,lw=.5)
    a.spines['top'].set_visible(False); a.spines['right'].set_visible(False)

a=ax[0,0]; a.plot(t,V/1000,color='#185FA5',lw=2,label='Velocity')
a.set_xlabel('Time from entry interface [s]'); a.set_ylabel('Velocity [km/s]',color='#185FA5')
a2=a.twinx(); a2.plot(t,h/1000,color='#D85A30',lw=2,ls='--',label='Altitude')
a2.set_ylabel('Altitude [km]',color='#D85A30'); a2.spines['top'].set_visible(False)
a.set_title(f'Allen-Eggers ballistic entry  ($\\beta$={beta:.0f} kg/m², $\\gamma$=-5.5°)',fontsize=11)

a=ax[0,1]; qh=sized['PICA'][3]
a.plot(t[:-1],qh/1e4,color='#185FA5',lw=2)
ip=np.argmax(qh)
a.plot(t[ip],qh[ip]/1e4,'o',ms=9,mfc='white',mew=2.5,color='#D85A30')
a.annotate(f'peak {qh[ip]/1e4:.1f} W/cm²\nt={t[ip]:.0f} s, h={h[ip]/1000:.0f} km\nM={M_traj[ip]:.1f}',
           xy=(t[ip],qh[ip]/1e4),xytext=(t[ip]+40,qh[ip]/1e4*.65),fontsize=9,color='#993C1D',
           arrowprops=dict(arrowstyle='->',color='#993C1D',lw=1.2))
a.set_xlabel('Time from entry interface [s]'); a.set_ylabel('Stagnation heat flux [W/cm²]')
a.set_title('Fay-Riddell convective heating',fontsize=11)

a=ax[1,0]
for nm,(L,Ts,Tb,qh,Tp) in sized.items():
    a.plot(t[:-1],Ts,color=MAT[nm]['c'],lw=2,label=f'{nm} surface')
    a.plot(t[:-1],Tb,color=MAT[nm]['c'],lw=1.4,ls='--',label=f'{nm} bondline')
a.axhline(523,color='#888780',ls=':',lw=1.6,label='Bondline limit 523 K')
a.set_xlabel('Time from entry interface [s]'); a.set_ylabel('Temperature [K]')
a.set_title('Surface and bondline response (sized thickness)',fontsize=11); a.legend(fontsize=7.5,ncol=2)

a=ax[1,1]
for nm,(L,Ts,Tb,qh,Tp) in sized.items():
    a.plot(np.linspace(0,L*100,len(Tp)),Tp,color=MAT[nm]['c'],lw=2,label=f'{nm} ({L*100:.1f} cm)')
a.axhline(523,color='#888780',ls=':',lw=1.6)
a.set_xlabel('Depth from heated surface [cm]'); a.set_ylabel('Temperature [K]')
a.set_title('Through-thickness profile at end of entry',fontsize=11); a.legend(fontsize=8.5)

f.suptitle('Transient TPS thermal analysis — Dragon-style capsule, LEO return',fontsize=13,y=1.00)
plt.tight_layout(); plt.savefig('/mnt/user-data/outputs/tps_thermal_analysis.png',dpi=150,bbox_inches='tight',facecolor='#FAFAFA')

np.savetxt('/mnt/user-data/outputs/trajectory_heating.csv',
  np.column_stack([t[:-1],h[:-1]/1000,V[:-1],M_traj[:-1],sized['PICA'][3]]),delimiter=',',
  header='time_s,altitude_km,velocity_ms,mach,heat_flux_Wm2',comments='')
print("\nsaved tps_thermal_analysis.png + trajectory_heating.csv")
