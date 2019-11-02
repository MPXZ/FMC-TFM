#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

def amplitude(temp,faqui,FMCh,N):
    #calculate the sampling point and store in array
    indh=np.ceil(temp*faqui)
    indh=np.where(indh<=1,2,indh)

    # for interpolation
    indl=indh-1
    indl=np.where(indl<=0,1,indl)

    #initialize array for interpolation
    Lh=np.zeros((temp.shape))
    Ll=np.zeros((temp.shape))

    npontos=FMCh.shape[2]


    for i in range(N):
        for j in range(N):
            #extract each TR A-scan amplitude information
            va=np.squeeze(FMCh[i,j,:])

            indhp=np.squeeze(indh[:,:,i,j])
            # if find point where indh>npontos, bring these points back to original points=0
            indhp=np.where((indhp>=npontos),0,indhp)
            indhp=indhp.astype(int)


            vaphm=np.zeros((indhp.shape[0],indhp.shape[1]))
            # take index point in indhp to find corresponding amplitude in each TR A-scan
            for m in range(indhp.shape[0]):
                for n in range(indhp.shape[1]):
                    vaphm[m,n]=va[indhp[m,n]]

            Lh[:, :, i, j] = vaphm


            indlp = np.squeeze(indl[:, :, i, j])
            indlp = np.where((indlp >= npontos), 0, indlp)
            indlp = indlp.astype(int)
        

            vaplm = np.zeros((indlp.shape[0], indlp.shape[1]))

            for k in range(indlp.shape[0]):
                for l in range(indlp.shape[1]):
                    vaplm[k, l] = va[indlp[k, l]]

            Ll[:,:,i,j]=vaplm


    # interpolation
    templ=indl/faqui
    htemp=((temp-templ)*(Lh-Ll))*faqui+Ll

    #sum up all the amplitude for each point in the grid and average on N^2
    I=np.sum(np.sum(htemp, axis=3), axis=2)/(N**2)

       
    return(I)


# In[ ]:




