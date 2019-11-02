#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pdb

def amplitude(temp,faqui,FMCh,N):
    indh=np.ceil(temp*faqui)
    indh=np.where(indh<=1,2,indh)


    indl=indh-1
    indl1=np.where(indl<=0,1,indl)

    Lh=np.zeros((temp.shape))
    Ll=np.zeros((temp.shape))

    npontos=FMCh.shape[2]
    
   

    for i in range(N):
        for j in range(N):
            va=np.squeeze(FMCh[i,j,:])

            indhp=np.squeeze(indh[:,:,i,j])
            indx=np.argwhere(indhp>npontos)  #return index of indhp where indhp > npontos
            

            # if find point where indh>npontos, bring these points back to original points=0
            lin=indx[:,0]
            col=indx[:,1]
            
            if indx==([]):
                pass
            else:
                for r in range(lin.size):
                    indhp[lin[r]][col[r]]=0
       
            
            indhpf=indhp.flatten().astype(int) #flatten indhp to 1-D array and convert float number to integer in array
            
          
            vaphm=[]
            for element in indhpf:
                vaphm.append(va[element]) #indhpf as index point to extract value in va as vaphm

            vaph1=np.array(vaphm)    #change vaphm list-->1-d array vaph1
            vaph=vaph1.reshape(indhp.shape)  # reshape vaph1 into 2-d array shape
            
            
            
            
            
            indlp=np.squeeze(indl[:,:,i,j])
            indx=np.argwhere(indlp>npontos)  #return index of indhp where indhp > npontos
        
            # if find point where indh>npontos, bring these points back to original points=0
            lin=indx[:,0]
            col=indx[:,1]
            
            if indx==([]):
                pass
            else:
                for r in range(lin.size):
                    indlp[lin[r]][col[r]]=0
       
            
            indlpf=indlp.flatten().astype(int) #flatten indhp to 1-D array and convert float number to integer in array
            
            vaplm=[]
            for element in indlpf:
                vaplm.append(va[element]) #indhpf as index point to extract value in va as vaphm

            vapl1=np.array(vaplm)    #change vaphm list-->1-d array vaph1
            vapl=vapl1.reshape(indlp.shape) 
            


            Lh[:,:,i,j]=vaph
            Ll[:,:,i,j]=vapl


            # create TFM image
    templ=indl/faqui
    htemp=((temp-templ)*(Lh-Ll))*faqui+Ll
   
    I=np.sum(np.sum(htemp,axis=3),axis=2)
       
    return(I)


# In[ ]:




