from astropy.io import ascii
import numpy as np

data=ascii.read('cat0p5z0p8_klt24_ilt25p5_SSFR_masscut8p64_0p50p7_sortSFR.dat')
my_range=np.arange(-1.49,3.04,0.01)
Cw=np.zeros(my_range.size)
Cwnorm=np.zeros(my_range.size)
Cnorm=np.zeros(my_range.size)
C=np.zeros(my_range.size)
N=np.zeros(my_range.size)
Nnorm=np.zeros(my_range.size)
Nwnorm=np.zeros(my_range.size)
Nw=np.zeros(my_range.size)

for j in range(my_range.size-1):
    for i in range(data['sfr_med'].size):
        if my_range[j]<=data['sfr_med'][i] and data['sfr_med'][i]<my_range[j+1]:
            N[j]+=1
        if j>0:
            C[j]=N[j]+C[j-1]    
# for j in range(my_range.size-1):
#     for i in range(data['mass_med'].size):
#         if my_range[j]<=data['mass_med'][i] and data['mass_med'][i]<my_range[j+1]:
#             Nw[j]+=10**(data['sfr_med'][i])
#             N[j]+=1
#     if j>0:
#         C[j]=N[j]+C[j-1]
#         Cw[j]=Nw[j]+Cw[j-1]
#Sw=np.sum(Nw)
S=np.sum(N)
C[-1]=S
#print Nw.shape
#Nwnorm=np.divide(Nw,Sw)
#Cwnorm=np.divide(Cw,Sw)
Nnorm=np.divide(N,S)
Cnorm=np.divide(C,S)
#print Sw
print S
#np.savetxt("Nmass_wsfr.txt",N)
ascii.write([my_range,N,C,Nnorm,Cnorm], 'SFRcum.dat', format='fixed_width', delimiter=' ')
#    print N[j]
#np.savetxt("Nmass_wsfr.txt",N)



 