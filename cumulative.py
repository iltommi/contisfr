import numpy as np

#funzione che calcola la cumulativa e la scrive in un file
def cumulative (vector, min, max, step) :
    """calcola la distribuzione cumulativa """
    my_range=np.arange(min,max,step)
    Cnorm=np.zeros(my_range.size)
    C=np.zeros(my_range.size)
    N=np.zeros(my_range.size)
    Nnorm=np.zeros(my_range.size)

    for j in range(my_range.size):
        for i in range(len(vector)):
            if my_range[j]<=vector[i] and vector[i]<my_range[j]+step:
                N[j]+=10**(vector[i])
            if j>0:
                C[j]=N[j]+C[j-1]
    
    S=np.sum(N)
    
    if int(S) != len(vector):
        print "cumulative left out ", len(vector) - int(S), "/", len(vector)

    Nnorm=np.divide(N,S)
    Cnorm=np.divide(C,S)
    
    return [my_range,N,C,Nnorm,Cnorm]
