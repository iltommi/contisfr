from astropy.io import ascii
import numpy as np

execfile('cumulative.py')

data=ascii.read('cat0p5z0p8_klt24_ilt25p5_SSFR_masscut8p64_0p50p7_sortSFR.dat')

my_range,N,C,Nnorm,Cnorm =  cumulative(data['sfr_med'],-1.49,3.03,0.01)

ascii.write([my_range,N,C,Nnorm,Cnorm], 'SFRcum.dat', format='fixed_width', delimiter=' ')



 