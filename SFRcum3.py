from astropy.io import ascii
import numpy as np
import random 

execfile('cumulative.py')


NmassGRB=ascii.read('NmassGRB.dat')
NMassGRBmeno3=ascii.read('NMassGRBmeno3.dat')

KS_d=[]
KS_p=[]



for i in range(1000):
    data_cumul=ascii.read('cumul'+str(nutil).zfill(3)+'.dat')
    data_cumul_clean=ascii.read('cumul_clean'+str(nutil).zfill(3)+'.dat')
    
    ks_test=scipy.stats.ks_2samp(NmassGRB['col4'],Cnorm)
    
    KS_d.append(ks_test[0])
    KS_p.append(ks_test[1])


