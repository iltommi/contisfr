from astropy.io import ascii
import numpy as np
import random 
import sys

execfile('cumulative.py')        

data=ascii.read('cat0p5z0p8_klt24_ilt25p5_SSFR_masscut8p64_0p50p7_sortSFR.dat')
datacum=ascii.read('SFRcum.dat')

print "done reading files"

nutil=0
failed=0


while nutil < 1000:
    mass_distr=[]
    n_number_good=0
    rejected=[]
    nutil_str=str(nutil).zfill(3)
    sys.stdout.write("case "+nutil_str+" : ")
    
    # tira numeri a caso finche' non arrivi a 13
    while n_number_good < 13:
        randVal=random.random() # numero a caso
        # controlliamo se j e' piu' grande dell'ultima, prendiamo l'ultima
        valFound=0
        if (randVal > datacum['col4'][-1]):
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
            if abs(data['sfr_med'][n] - valFound) < 0.005:
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
        print "rejected = ", rejected
    else:
        print "ok"
    # metti in ordine la scrivania!
    mass_distr.sort()
    # e togli i due piu' grossi
    mass_distr_clean=mass_distr[0:-2]

    #calcola le due cumulative
    cumul_plain=cumulative(mass_distr, 8.6,11.7,0.1)
    cumul_clean=cumulative(mass_distr_clean, 8.6,11.7,0.1)
    
    # e scrivile
    ascii.write(cumul_plain, 'cumul_plain'+nutil_str+'.dat', format='fixed_width', delimiter=' ')
    ascii.write(cumul_clean, 'cumul_clean'+nutil_str+'.dat', format='fixed_width', delimiter=' ')

    

    nutil += 1
    
print "failed times: ", failed


