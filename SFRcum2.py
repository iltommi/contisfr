from astropy.io import ascii
import numpy as np
import random 

execfile('cumulative.py')        

data=ascii.read('cat0p5z0p8_klt24_ilt25p5_SSFR_masscut8p64_0p50p7_sortSFR.dat')
datacum=ascii.read('SFRcum.dat')

print "done reading files"

nutil=0
failed=0
while nutil < 1000:
    mass_distr=[]
    n_number_rnd=0
    while n_number_rnd < 13:
        randVal=random.random()
        for j in range(datacum['col4'].size-1):
            if datacum['col4'][j] <= randVal and randVal < datacum['col4'][j+1]:
                vals=[]
                for n in range(data['sfr_med'].size) :
                    if data['sfr_med'][n] == datacum['col0'][j]:
                        vals.append(data['mass_med'][n])
                
                if len(vals) == 0:
                    print "for ", randVal, " sfr_med empty for ", datacum['col0'][j]
                else:
                    n_number_rnd+=1
                    nth=random.randrange(0,len(vals))
#                    print randVal, datacum['col0'][j], len(vals), nth
                    mass_distr.append(vals[nth])
        
    mass_distr.sort()

    mass_distr_clean=mass_distr[0:-2]

    nutil_str=str(nutil).zfill(3)
    cumulative(mass_distr, 8.6,11.7,0.1, 'cumul'+nutil_str+'.dat')
    cumulative(mass_distr_clean, 8.6,11.7,0.1, 'cumul_clean'+nutil_str+'.dat')

    nutil += 1
    

print "failed times: ", failed


