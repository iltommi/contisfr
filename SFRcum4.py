from astropy.io import ascii
import numpy as np
import random 
import sys
import scipy.stats


#execfile('cumulative.py')        

#data=ascii.read('cat0p5z0p8_klt24_ilt25p5_SSFR_masscut8p64_0p50p7_sortSFR.dat')
datacum=ascii.read('cumulative_zbinadded.dat')

masseGRB=ascii.read('masse_recap_2aprile_Lk22mai.txt')


masseGRB.sort(["Mass"]) 


print "done reading files"

nutil=0
failed=0

np.set_printoptions(precision=3, linewidth=10000)

KS_d_plain=[]
KS_p_plain=[]
KS_d_clean=[]
KS_p_clean=[]

while nutil < 100:
    mass_distr=[]
    n_number_good=0
    rejected=[]
    nutil_str=str(nutil).zfill(3)
    sys.stdout.write("case "+nutil_str+" : ")
    
    # tira numeri a caso finche' non arrivi a 13
    while n_number_good < 14:
        randVal=random.random() # numero a caso
        # controlliamo se j e' piu' grande dell'ultima, prendiamo l'ultima
        valFound=0
        
        if (randVal >= datacum['Cwtot'][-1]):
            valFound=datacum['M_bin'][-1]
        else:
            # guarda tra tutti i valori della col4 ...
            for j in range(datacum['Cwtot'].size-1):
                # ... e trova il j per cui randVal sta bello bello in mezzo
                if datacum['Cwtot'][j] <= randVal and randVal < datacum['Cwtot'][j+1]: 
                    valFound=datacum['M_bin'][j]
        
        mass_distr.append(valFound)
                
        n_number_good +=1
    # metti in ordine la scrivania!
    mass_distr.sort()
    # scrivi qualcosa che fa fico
    print np.array(mass_distr)
    # e togli i due piu' grossi
    mass_distr_clean=mass_distr[0:-2]


    ks_test_plain = scipy.stats.ks_2samp(masseGRB['Mass'],mass_distr)
    KS_d_plain.append(ks_test_plain[0])
    KS_p_plain.append(ks_test_plain[1])
    ks_test_clean = scipy.stats.ks_2samp(masseGRB['Mass'],mass_distr_clean)
    KS_d_clean.append(ks_test_clean[0])
    KS_p_clean.append(ks_test_clean[1])
    
    nutil += 1

allData=[KS_d_plain, KS_p_plain, KS_d_clean, KS_p_clean]

for data in allData:
    test_good = sum(1 if x > 0.01 else 0 for x in data)
    print "KS ", test_good

ascii.write(allData, 'KS.dat', format='fixed_width', delimiter=' ')

print "failed times: ", failed


