import numpy as np, matplotlib.pyplot as plt
g,R=1.4,287.058
def fs(M,P,T):
    rho=P/(R*T); a=np.sqrt(g*R*T); V=M*a; q=.5*rho*V**2
    A=((g+1)**2*M**2)/(4*g*M**2-2*(g-1)); B=(1-g+2*g*M**2)/(g+1)
    P02=P*A**(g/(g-1))*B
    P0f=P*(1+(g-1)/2*M**2)**(g/(g-1))
    return dict(rho=rho,V=V,q=q,P02=P02,P0f=P0f,cp=(P02-P)/q)

C={5.0:dict(P=287.14,T=250.35,alt=40,Pw=9262.0,P0=152513.81),
   7.5:dict(P=149.10,T=264.16,alt=45,Pw=11172.6,P0=966595.44),
   10.0:dict(P=79.78,T=270.65,alt=50,Pw=10248.8,P0=3421983.5)}

rows=[]
for M,c in C.items():
    t=fs(M,c['P'],c['T'])
    cp=(c['Pw']-c['P'])/t['q'] if c['Pw'] else None
    rows.append(dict(M=M,alt=c['alt'],q=t['q'],V=t['V'],
        Pw=c['Pw'],Pw_t=t['P02'],Pw_e=abs(c['Pw']-t['P02'])/t['P02']*100 if c['Pw'] else None,
        cp=cp,cp_t=t['cp'],cp_e=abs(cp-t['cp'])/t['cp']*100 if cp else None,
        P0=c['P0'],P0_t=t['P0f'],P0_e=abs(c['P0']-t['P0f'])/t['P0f']*100 if c['P0'] else None))

print(f"{'M':>5} {'alt':>4} {'V m/s':>8} {'q Pa':>8} | {'Pw CFD':>9} {'Pw th':>9} {'err%':>6} | {'Cp':>6} {'Cp th':>6} {'err%':>6} | {'P0 CFD':>10} {'P0 th':>10} {'err%':>6}")
print("-"*118)
for r in rows:
    f=lambda v,d=1: f"{v:,.{d}f}" if v is not None else "pending"
    print(f"{r['M']:>5.1f} {r['alt']:>4} {r['V']:>8.0f} {r['q']:>8.0f} | {f(r['Pw']):>9} {f(r['Pw_t']):>9} {f(r['Pw_e'],2):>6} | {f(r['cp'],3):>6} {f(r['cp_t'],3):>6} {f(r['cp_e'],2):>6} | {f(r['P0'],0):>10} {f(r['P0_t'],0):>10} {f(r['P0_e'],2):>6}")

B='#185FA5'; O='#D85A30'; G='#1D9E75'; Gy='#888780'
f,ax=plt.subplots(1,3,figsize=(15,4.8)); f.patch.set_facecolor('#FAFAFA')
for a in ax:
    a.set_facecolor('#FAFAFA'); a.grid(ls='--',alpha=.35,lw=.5)
    a.spines['top'].set_visible(False); a.spines['right'].set_visible(False)
Ms=np.linspace(4.5,10.8,200)
have=[r for r in rows if r['Pw'] is not None]
pend=[r for r in rows if r['Pw'] is None]

# 1 peak wall static P
th=[fs(m,np.interp(m,[5,7.5,10],[287.14,149.10,79.78]),np.interp(m,[5,7.5,10],[250.35,264.16,270.65]))['P02'] for m in Ms]
ax[0].plot(Ms,th,color=G,ls='--',lw=1.6,label='Rayleigh Pitot theory')
ax[0].plot([r['M'] for r in have],[r['Pw'] for r in have],'o',ms=10,mfc='white',mew=2.5,color=B,label='CFD',zorder=5)
for r in have: ax[0].annotate(f"{r['Pw']:,.0f} Pa\n{r['Pw_e']:.2f}% err",(r['M'],r['Pw']),xytext=(0,-42),textcoords='offset points',ha='center',fontsize=8.5,color=B)
for r in pend: ax[0].plot(r['M'],r['Pw_t'],'o',ms=9,mfc='none',mew=1.6,color=Gy); ax[0].annotate('pending',(r['M'],r['Pw_t']),xytext=(0,14),textcoords='offset points',ha='center',fontsize=8,color=Gy)
ax[0].set_ylabel('Peak wall static pressure [Pa]'); ax[0].set_title('Stagnation-point pressure',fontsize=11)

# 2 peak Cp
thc=[fs(m,np.interp(m,[5,7.5,10],[287.14,149.10,79.78]),np.interp(m,[5,7.5,10],[250.35,264.16,270.65]))['cp'] for m in Ms]
ax[1].plot(Ms,thc,color=G,ls='--',lw=1.6,label='Newtonian limit')
ax[1].plot([r['M'] for r in have],[r['cp'] for r in have],'o',ms=10,mfc='white',mew=2.5,color=B,label='CFD',zorder=5)
for r in have: ax[1].annotate(f"{r['cp']:.3f}\n{r['cp_e']:.2f}% err",(r['M'],r['cp']),xytext=(0,-42),textcoords='offset points',ha='center',fontsize=8.5,color=B)
for r in pend: ax[1].plot(r['M'],r['cp_t'],'o',ms=9,mfc='none',mew=1.6,color=Gy); ax[1].annotate('pending',(r['M'],r['cp_t']),xytext=(0,14),textcoords='offset points',ha='center',fontsize=8,color=Gy)
ax[1].set_ylabel('Peak pressure coefficient $C_p$'); ax[1].set_title('Stagnation-point $C_p$',fontsize=11); ax[1].set_ylim(1.75,1.88)

# 3 freestream P0 (log)
thp=[fs(m,np.interp(m,[5,7.5,10],[287.14,149.10,79.78]),np.interp(m,[5,7.5,10],[250.35,264.16,270.65]))['P0f'] for m in Ms]
ax[2].semilogy(Ms,thp,color=G,ls='--',lw=1.6,label='Isentropic theory')
h2=[r for r in rows if r['P0'] is not None]
ax[2].semilogy([r['M'] for r in h2],[r['P0'] for r in h2],'o',ms=10,mfc='white',mew=2.5,color=B,label='CFD',zorder=5)
for r in h2: ax[2].annotate(f"{r['P0']/1000:,.1f} kPa\n{r['P0_e']:.2f}% err",(r['M'],r['P0']),xytext=(0,-42),textcoords='offset points',ha='center',fontsize=8.5,color=B)
for r in [x for x in rows if x['P0'] is None]:
    ax[2].semilogy(r['M'],r['P0_t'],'o',ms=9,mfc='none',mew=1.6,color=Gy)
    ax[2].annotate('pending',(r['M'],r['P0_t']),xytext=(0,14),textcoords='offset points',ha='center',fontsize=8,color=Gy)
ax[2].set_ylabel('Freestream total pressure $P_0$ [Pa]'); ax[2].set_title('Freestream $P_0$ (BC validation)',fontsize=11)

for a in ax: a.set_xlabel('Mach number'); a.legend(fontsize=8.5,loc='best')
f.suptitle('CFD validation vs analytical theory — Dragon capsule, k-ω SST, 479k cells',fontsize=12,y=1.005)
plt.tight_layout(); plt.savefig('/mnt/user-data/outputs/validation_mach_sweep.png',dpi=150,bbox_inches='tight',facecolor='#FAFAFA')
print("\nsaved validation_mach_sweep.png")
