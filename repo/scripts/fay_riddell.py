import numpy as np, matplotlib.pyplot as plt

g,R,Pr,cp_air=1.4,287.058,0.71,1004.5
def mu_suth(T): return 1.458e-6*T**1.5/(T+110.4)

# --- fit nose radius from CFD surface points -------------------------------
d=np.genfromtxt('/mnt/user-data/uploads/cp_mach5_komega.csv',skip_header=1)
x,y,z=d[:,1],d[:,2],d[:,3]; r=np.sqrt(x**2+z**2)
hs=y<0.55                                   # heat-shield cap only
# sphere cap:  R = (a^2 + h^2)/(2h)
a_max=r[hs].max(); h=y[hs].max()-y[hs].min()
Rn=(a_max**2+h**2)/(2*h)
print(f"Heat-shield fit:  a={a_max:.3f} m  h={h:.3f} m  ->  R_n = {Rn:.3f} m\n")

def normal_shock(M,P1,T1):
    P2=P1*(1+2*g/(g+1)*(M**2-1))
    M2=np.sqrt((M**2+2/(g-1))/(2*g/(g-1)*M**2-1))
    T2=T1*(1+2*g/(g+1)*(M**2-1))*((2+(g-1)*M**2)/((g+1)*M**2))
    P02=P2*(1+(g-1)/2*M2**2)**(g/(g-1))
    T0=T1*(1+(g-1)/2*M**2)
    return P02,T0,P2,T2

def fay_riddell(M,P_inf,T_inf,Rn,Tw=300.0):
    rho_inf=P_inf/(R*T_inf); V=M*np.sqrt(g*R*T_inf)
    Pe,T0,_,_=normal_shock(M,P_inf,T_inf)
    rho_e=Pe/(R*T0);  mu_e=mu_suth(T0)
    rho_w=Pe/(R*Tw);  mu_w=mu_suth(Tw)
    dudx=(1/Rn)*np.sqrt(2*(Pe-P_inf)/rho_e)      # Newtonian vel. gradient
    h0=cp_air*T0; hw=cp_air*Tw
    q=0.763*Pr**-0.6*(rho_e*mu_e)**0.4*(rho_w*mu_w)**0.1*np.sqrt(dudx)*(h0-hw)
    return q, T0, dudx, V, rho_inf

def sutton_graves(V,rho_inf,Rn): return 1.7415e-4*np.sqrt(rho_inf/Rn)*V**3

# trajectory: Mach vs altitude (matches CFD cases)
Mtab=np.array([5,7.5,10,15,20,25])
Ptab=np.array([287.14,149.10,79.78,21.96,5.221,2.388])
Ttab=np.array([250.35,264.16,270.65,247.02,219.59,208.40])
Alt =np.array([40,45,50,60,70,75])

print(f"{'M':>5} {'alt':>4} {'V m/s':>7} {'T0 K':>8} {'q_FR':>10} {'q_SG':>10} {'diff%':>7}")
print("-"*60)
res=[]
for M,P,T,A in zip(Mtab,Ptab,Ttab,Alt):
    q,T0,dudx,V,rho=fay_riddell(M,P,T,Rn)
    qs=sutton_graves(V,rho,Rn)
    res.append((M,A,V,T0,q,qs))
    print(f"{M:>5.1f} {A:>4} {V:>7.0f} {T0:>8.0f} {q/1e4:>8.2f} W/cm² {qs/1e4:>6.2f} W/cm² {abs(q-qs)/qs*100:>6.1f}")

res=np.array(res)
Mf=np.linspace(5,25,120)
qf=[];qg=[]
for m in Mf:
    P=np.interp(m,Mtab,Ptab); T=np.interp(m,Mtab,Ttab)
    q,_,_,V,rho=fay_riddell(m,P,T,Rn); qf.append(q/1e4); qg.append(sutton_graves(V,rho,Rn)/1e4)

B='#185FA5';O='#D85A30';G='#1D9E75';Gy='#888780'
f,(a1,a2)=plt.subplots(1,2,figsize=(13.5,5.2)); f.patch.set_facecolor('#FAFAFA')
for a in (a1,a2):
    a.set_facecolor('#FAFAFA');a.grid(ls='--',alpha=.35,lw=.5)
    a.spines['top'].set_visible(False);a.spines['right'].set_visible(False);a.set_xlabel('Mach number')

a1.plot(Mf,qf,color=B,lw=2.2,label='Fay-Riddell')
a1.plot(Mf,qg,color=O,lw=1.6,ls='--',label='Sutton-Graves')
a1.axvspan(5,10,alpha=.10,color=G,label='CFD-validated range')
a1.axvline(12,color=Gy,ls=':',lw=1.4)
a1.annotate('real-gas dissociation\nsignificant above ~M12',xy=(12,max(qf)*.55),xytext=(13.2,max(qf)*.30),
            fontsize=8.5,color=Gy,arrowprops=dict(arrowstyle='->',color=Gy,lw=1))
a1.plot(res[:,0],res[:,4]/1e4,'o',ms=7,mfc='white',mew=2,color=B,zorder=5)
a1.set_ylabel('Stagnation heat flux [W/cm²]')
a1.set_title(f'Stagnation-point heating, $R_n$ = {Rn:.2f} m, $T_w$ = 300 K',fontsize=11)
a1.legend(fontsize=9)

a2.plot(Mf,[np.interp(m,Mtab,Ttab)*(1+.2*m**2) for m in Mf],color=B,lw=2.2,label='Perfect gas $T_0$')
a2.axvspan(5,10,alpha=.10,color=G,label='CFD-validated range')
a2.axhline(2500,color=O,ls='--',lw=1.4,label='PICA surface limit (~2500 K)')
a2.axvline(12,color=Gy,ls=':',lw=1.4)
a2.annotate('perfect-gas $T_0$ over-predicts\n(energy goes to dissociation)',xy=(18,np.interp(18,Mtab,Ttab)*(1+.2*324)),
            xytext=(11.5,26000),fontsize=8.5,color=Gy,arrowprops=dict(arrowstyle='->',color=Gy,lw=1))
a2.set_ylabel('Stagnation temperature $T_0$ [K]')
a2.set_title('Shock-layer stagnation temperature',fontsize=11); a2.legend(fontsize=9)

plt.tight_layout();plt.savefig('/mnt/user-data/outputs/fay_riddell_heating.png',dpi=150,bbox_inches='tight',facecolor='#FAFAFA')
np.savetxt('/mnt/user-data/outputs/fay_riddell_results.csv',res,delimiter=',',
    header='Mach,altitude_km,V_ms,T0_K,q_FayRiddell_Wm2,q_SuttonGraves_Wm2',comments='')
print("\nsaved fay_riddell_heating.png + fay_riddell_results.csv")
