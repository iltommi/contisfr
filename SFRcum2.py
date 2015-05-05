from astropy.io import ascii
import numpy as np
import random 


data=ascii.read('cat0p5z0p8_klt24_ilt25p5_SSFR_masscut8p64_0p50p7_sortSFR.dat')
datacum=ascii.read('SFRcum.dat')

NmassGRB=ascii.read('NmassGRB.dat')
NMassGRBmeno3=ascii.read('NMassGRBmeno3.dat')


print "done reading files"
print "size",datacum['col4'].size

nutil=0
while nutil < 1000:
    mass_distr=[]
    randomVec=np.random.rand(13)
    for randVal in randomVec:
        for j in range(datacum['col4'].size-1):
            if datacum['col4'][j] <= randVal and randVal < datacum['col4'][j+1]:
                vals=[]
                for n in range(data['sfr_med'].size) :
                    if data['sfr_med'][n] == datacum['col0'][j]:
                        vals.append(data['mass_med'][n])
                
                if len(vals) == 0:
                    print "for ", randVal, " sfr_med empty for ", datacum['col0'][j]
                else:
                    nth=random.randrange(0,len(vals))
                    print randVal, datacum['col0'][j], len(vals), nth
                    mass_distr.append(vals[nth])

    if len(mass_distr) > 0:

        mass_distr.sort()

        mass_distr_clean=mass_distr[0:-2]
    
        my_range=np.arange(8.6,11.7,0.1)
        Cnorm=np.zeros(my_range.size)
        C=np.zeros(my_range.size)
        N=np.zeros(my_range.size)
        Nnorm=np.zeros(my_range.size)
    
        for j in range(my_range.size-1):
            for i in range(len(mass_distr_clean)):
                if my_range[j]<=mass_distr_clean[i] and mass_distr_clean[i]<my_range[j+1]:
                    N[j]+=1
                if j>0:
                    C[j]=N[j]+C[j-1]    
        S=np.sum(N)
        C[-1]=S
        Nnorm=np.divide(N,S)
        Cnorm=np.divide(C,S)
        fname='cumul_clean'+str(nutil).zfill(3)+'.dat'
        print fname, " S = ",  S
        ascii.write([my_range,N,C,Nnorm,Cnorm], fname, format='fixed_width', delimiter=' ')
        nutil=nutil+1
    else :
        print "rejecting"



