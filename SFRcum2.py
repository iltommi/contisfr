from astropy.io import ascii
import numpy as np
import random 
import sys
import scipy.stats


execfile('cumulative.py')        

data=ascii.read('cat0p5z0p8_klt24_ilt25p5_SSFR_masscut8p64_0p50p7_sortSFR.dat')
datacum=ascii.read('SFRcum.dat')

NmassGRB=ascii.read('NmassGRB.dat')
NMassGRBmeno3=ascii.read('NMassGRBmeno3.dat')
masseGRB=ascii.read('masse_recap_2aprile_Lk22mai.txt')
masseGRB8p64=ascii.read('masse_recap_2aprile_Lk22mai8p64.txt')


masseGRB.sort(["Mass"]) 
masseGRB8p64.sort(["Mass"]) 

#NMassGRBcut8p65=ascii.read('NmassGRBcut8p65.dat')


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
    while n_number_good < 16:
        randVal=random.random() # numero a caso
        # controlliamo se j e' piu' grande dell'ultima, prendiamo l'ultima
        valFound=0
        if (randVal >= datacum['col4'][-1]):
            valFound=datacum['col0'][-1]
        else:
            # guarda tra tutti i valori della col4 ...
            for j in range(datacum['col4'].size-1):
                # ... e trova il j per cui randVal sta bello bello in mezzo
                if datacum['col4'][j] <= randVal and randVal < datacum['col4'][j+1]: 
                    valFound=datacum['col0'][j]
            
        
        #inizializza un vettore vuoto dove metteremo tutti gli sfr_med +- uguali a valFound
        vals=[] 
        # tra tutte le sfr_med ... 
        for n in range(data['sfr_med'].size) : 
             # prendi quelle che sono uguali a quello trovato
            if abs(data['sfr_med'][n] - valFound) < 0.05:
                vals.append(data['mass_med'][n])

        # eh beh non sempre te le trovi ...
        if len(vals) == 0:

            failed += 1

            rejected.append((randVal,valFound))
        else: 
            # ... ma spesso si'
            n_number_good+=1
            # prendi un numero a caso 
            nth=random.randrange(0,len(vals)) 
            # e aggiungilo al vettore mass_distr
            mass_distr.append(vals[nth])
                
                
    # scrivi qualcosa che fa fico
    if len(rejected) > 0: 
        print "rejected = ", 
        for rej in rejected:
            print np.array(rej) ,
        print ""
    else:
        print "ok"
    # metti in ordine la scrivania!
    mass_distr.sort()
    print np.array(mass_distr)
    # e togli i due piu' grossi
    mass_distr_clean=mass_distr[0:-2]


    ks_test_plain = scipy.stats.ks_2samp(masseGRB['Mass'],mass_distr)
    KS_d_plain.append(ks_test_plain[0])
    KS_p_plain.append(ks_test_plain[1])
    ks_test_clean = scipy.stats.ks_2samp(masseGRB['Mass'],mass_distr_clean)
    KS_d_clean.append(ks_test_clean[0])
    KS_p_clean.append(ks_test_clean[1])
    
#     #calcola le due cumulative
# #    cumul_plain=cumulative(mass_distr, 8.6,13.0,0.1)
# #    cumul_clean=cumulative(mass_distr_clean, 8.6,13.0,0.1)
#     
#     # e scrivile
# #    ascii.write(cumul_plain, 'cumul_plain'+nutil_str+'.dat', format='fixed_width', delimiter=' ')
# #    ascii.write(cumul_clean, 'cumul_clean'+nutil_str+'.dat', format='fixed_width', delimiter=' ')
#     ascii.write(mass_distr, 'mass_distr'+nutil_str+'.dat', format='fixed_width', delimiter=' ')
#     ascii.write(mass_distr_clean, 'mass_distr_clean'+nutil_str+'.dat', format='fixed_width', delimiter=' ')

    

    nutil += 1

allData=[KS_d_plain, KS_p_plain, KS_d_clean, KS_p_clean]

for data in allData:
    test_good = sum(1 if x > 0.01 else 0 for x in data)
    print "KS ", test_good

ascii.write(allData, 'KS.dat', format='fixed_width', delimiter=' ')

print "failed times: ", failed


