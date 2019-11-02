#!/usr/bin/env python
# coding: utf-8

# In[1]:
import numpy as np
from scipy import signal
from scipy.signal import hilbert, chirp



def FMC(N, f0,fa,rd):
    npontos = round(rd.shape[0] / N)  # number of samples for each A-scan
    FMCbruta = np.zeros((N, N, npontos), dtype=float)  # initializ raw data
    vet = np.zeros((npontos, 1), dtype=float)  # create a vector to operate

    for i in range(N):  # Emission
        for j in range(N):  # reception

            vet[:, 0] = rd[npontos * i:npontos * (i + 1), j]
            FMCbruta[i, j, :] = vet[:, 0]
            FMCbruta = np.where(np.isinf(FMCbruta), 0, FMCbruta)

    # FMC filtering

    b, a = signal.butter(4, [(0.2 * f0 * 2) / fa, (2 * f0 * 2) / fa], 'bandpass')
    FMC = np.zeros((N, N, npontos), dtype=float)
    FMCh = FMC

    for i in range(N):
        for j in range(N):
            FMCh[i, j, :] = signal.filtfilt(b, a, FMCbruta[i, j, :])


    return (FMCh)

# In[ ]:



