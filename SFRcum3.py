from astropy.io import ascii
import numpy as np
import random 
import scipy.stats
import os.path
execfile('cumulative.py')


NmassGRB=ascii.read('NmassGRB.dat')
NMassGRBmeno3=ascii.read('NMassGRBmeno3.dat')

print "done reading files"

stub_file=('cumul_plain', 'cumul_clean')

# cicla tra 'sti due pzzi di file qui sopra
for stub in stub_file:
    KS_d=[]
    KS_p=[]

    # conta fino a mille
    for i in range(1000):
        # prendi il nome file
        fname=stub + str(i).zfill(3) + '.dat'        
        print fname
        # il file esiste?
        if os.path.isfile(fname) :
            # leggilo
            data_cumul=ascii.read(fname)
        
            # calcola il KS
            ks_test_plain = scipy.stats.ks_2samp(NmassGRB['col4'],data_cumul['col3'])
    
            # mettiti da parte 
            
            KS_d.append(ks_test_plain[0])
            KS_p.append(ks_test_plain[1])

    # calcola le cumulative
    test_good = sum(1 if x > 0.01 else 0 for x in KS_p)
    
    print stub, "test ok", test_good

    
    cumul_KS_d=cumulative(KS_d, 0, 1, 0.1)  # <<<<<<<<<<<<<<<<<< REPLACE ME
    cumul_KS_p=cumulative(KS_p, 0, 1, 0.1)  # <<<<<<<<<<<<<<<<<< REPLACE ME
    
    # scrivile
    ascii.write(cumul_KS_d, stub+"KS_d.dat", format='fixed_width', delimiter=' ')
    ascii.write(cumul_KS_p, stub+"KS_p.dat", format='fixed_width', delimiter=' ')


# ciao bello!