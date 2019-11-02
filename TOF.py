#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pdb


def Time_of_flight(xpmin,xpmax,N,pitch,c2,ZPmin,ZPmax,resolution):
    
    sarray=(N-1)*pitch    #size of array
   
    Gx,Gz,Xt=np.mgrid[xpmin:xpmax+resolution:31j,ZPmin:ZPmax+resolution:resolution,-sarray/2:sarray/2+pitch:pitch]
    Zt=np.zeros((Xt.shape))
    

    sgx=Gx.shape[0]
    sgz=Gx.shape[1]

    #transducer --> focal point
    Di1=np.sqrt((Gx-Xt)**2+(Gz-Zt)**2)


    # focal point --> transducer
    Dv1=Di1

    #time of flight of each point in the block
    tempi=Di1/c2
    tempv=tempi

    #time of flight from transmitting
    tempia=np.tile(tempi,(1,1,N))  #Construct an array by repeating tempi the number of times given by reps(1,1,N).
    tempia2=np.reshape(tempia,(sgx,sgz,N,N))

    #time of flight from reciving
    tempva=np.tile(tempv,(1,1,N))
    tempva2=np.reshape(tempva,(sgx,sgz,N,N))
    tempva3=tempva2.swapaxes(3,2)

    #temp is a 4-d array [nxpoint,nzpoint,N,N]
    temp=tempia2+tempva3

    return(temp)

