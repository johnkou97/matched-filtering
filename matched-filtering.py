import os
import numpy as np
import scipy 
import matplotlib.pyplot as plt
np.seterr(divide='ignore')
np.seterr(invalid='ignore')


mas=np.arange(1,100,0.5)
phiran=np.arange(0,2*np.pi,0.2)


def templ(phi_c,x,t,tc):
    resul=np.nan_to_num((tc-t)**(-1/4)*np.cos(phi_c-39.11*x**(-5/8)*(tc-t)**(5/8)))
    resul[abs(resul)>10**(4)]=0
    return resul


def match_filter(signal):
    sn=[]
    for i in mas:
        for j in phiran:
            for k in range(len(time)):
                tc=time[k]
                filt=templ(j,i,time,tc)
                val=(np.dot(filt,signal))**2
                sn.append(np.amax(val))

    
    max_loc=np.where(sn==np.amax(sn))[0][0]
    count=0
    for i in mas:
        for j in phiran:
            for k in range(len(time)):
                count=count+1
                if count==max_loc:
                    break
            if count==max_loc:
                break
        if count==max_loc:
            break
    mass_true=i
    phi_c_true=j

    tsn=[]
    count=0
    for i in mas:
        for j in phiran:
            for k in range(len(time)):
                if (i==mass_true) & (j==phi_c_true):
                    tsn.append(sn[count])
                count=count+1

    mpsn=[]
    count=0
    for i in mas:
        psn=[]
        for j in phiran:
            ttsn=[]
            for k in range(len(time)):
                ttsn.append(sn[count])
                count=count+1
            psn.append(np.amax(ttsn))
        mpsn.append(psn)
    return  sn, mpsn, tsn


data=np.loadtxt('AllWithNoise.dat').T

time=data[0]
strain1=data[1]
strain2=data[2]
strain3=data[3]

print('Running match filtering for strain 1')
sn_1, mpsn_1, tsn_1 = match_filter(strain1)
print('Running match filtering for strain 2')
sn_2, mpsn_2, tsn_2 = match_filter(strain2)
print('Running match filtering for strain 3')
sn_3, mpsn_3, tsn_3 = match_filter(strain3)


# create results folder
if not os.path.exists('results'):
    os.makedirs('results')



np.save('results/mass_sampling.npy',mas)
np.save('results/phi_sampling.npy',phiran)
np.save('results/sn_strain1.npy',sn_1)
np.save('results/time_sn_strain1.npy',tsn_1)
np.save('results/mass_phi_sn_strain1.npy',mpsn_1)
np.save('results/sn_strain2.npy',sn_2)
np.save('results/time_sn_strain2.npy',tsn_2)
np.save('results/mass_phi_sn_strain2.npy',mpsn_2)
np.save('results/sn_strain3.npy',sn_3)
np.save('results/time_sn_strain3.npy',tsn_3)
np.save('results/mass_phi_sn_strain3.npy',mpsn_3)
