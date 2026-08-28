import numpy as np, matplotlib.pyplot as plt
g,R=1.4,287.058
def th(M,P,T):
    rho=P/(R*T);V=M*np.sqrt(g*R*T);q=.5*rho*V**2
    A=((g+1)**2*M**2)/(4*g*M**2-2*(g-1));B=(1-g+2*g*M**2)/(g+1)
    P02=P*A**(g/(g-1))*B; return P02,q,(P02-P)/q

def load(f,resc=None):
    d=np.genfromtxt(f,skip_header=1,delimiter=',' if '7p5' in f else None)
    x,y,z,cp=d[:,1],d[:,2],d[:,3],d[:,5]
    if resc: cp=(cp*0.6125-resc[0])/resc[1]
    return x,y,z,np.sqrt(x**2+z**2),cp

P5,q5,c5=th(5,287.14,250.35); P7,q7,c7=th(7.5,149.10,264.16); P10,q10,c10=th(10,79.78,270.65)
D={5.0:(load('/mnt/user-data/uploads/cp_mach5_komega.csv',(287.14,q5)),c5,'#185FA5'),
   7.5:(load('/mnt/user-data/uploads/cp_mach7p5_komega.csv'),c7,'#1D9E75'),
   10.0:(load('/mnt/user-data/uploads/cp_mach10_komega.csv'),c10,'#D85A30')}

Rn=3.248; Gy='#888780'
print(f"{'M':>5} {'n':>7} {'Cp max':>8} {'theory':>8} {'AWA hs':>8}")
for M,((x,y,z,r,cp),ct,col) in D.items():
    hs=y<0.6
    print(f"{M:>5.1f} {len(cp):>7d} {cp.max():>8.3f} {ct:>8.3f} {cp[hs].mean():>8.3f}")

f,(a1,a2)=plt.subplots(1,2,figsize=(13.5,5.2)); f.patch.set_facecolor('#FAFAFA')
for a in (a1,a2):
    a.set_facecolor('#FAFAFA');a.grid(ls='--',alpha=.35,lw=.5)
    a.spines['top'].set_visible(False);a.spines['right'].set_visible(False)

for M,((x,y,z,r,cp),ct,col) in D.items():
    a1.scatter(y,cp,s=.9,c=col,alpha=.28)
    a1.axhline(ct,color=col,ls='--',lw=1.1)
    a1.plot([],[],'o',color=col,ms=7,label=f'Mach {M:g}')
a1.axhline(0,color=Gy,lw=.6)
a1.set_xlabel('Y position along flow axis [m]');a1.set_ylabel('Pressure coefficient $C_p$')
a1.set_title('$C_p$ over capsule surface — three Mach numbers',fontsize=11)
a1.annotate('heat shield\n(stagnation)',xy=(.1,1.72),xytext=(1.05,1.52),fontsize=8.5,color=Gy,
            arrowprops=dict(arrowstyle='->',color=Gy,lw=1))
a1.annotate('shoulder expansion',xy=(.85,.12),xytext=(1.55,.68),fontsize=8.5,color=Gy,
            arrowprops=dict(arrowstyle='->',color=Gy,lw=1))
a1.legend(fontsize=9)

tt=np.linspace(0,np.arcsin(min(1,1.799/Rn)),120)
for M,((x,y,z,r,cp),ct,col) in D.items():
    hs=y<0.6
    a2.scatter(r[hs],cp[hs],s=2.5,c=col,alpha=.35)
    a2.plot(Rn*np.sin(tt),ct*np.cos(tt)**2,color=col,lw=2,label=f'Newtonian M{M:g}')
a2.set_xlabel('Radial distance from axis [m]');a2.set_ylabel('Pressure coefficient $C_p$')
a2.set_title(f'Heat-shield $C_p$ vs modified Newtonian ($R_n$ = {Rn:.2f} m)',fontsize=11)
a2.legend(fontsize=8.5)

f.suptitle('Surface pressure distribution — Dragon capsule, k-ω SST, 479k cells',fontsize=12,y=1.01)
plt.tight_layout();plt.savefig('/mnt/user-data/outputs/cp_comparison_3mach.png',dpi=150,bbox_inches='tight',facecolor='#FAFAFA')
print("saved")
