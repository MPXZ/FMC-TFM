import numpy as np
import csv


def read_csv(filename):
    with open(filename, 'r') as f:
        readers = csv.reader(f, delimiter=';')
        x = list(readers)
        del (x[0:17])

        rd = np.array(x)
        time=rd[:,1].astype(float)
        faqui=round(1e6/(time[1]-time[0]))

        #delete last column
        rd=np.delete(rd,-1,1)
        rd = rd[:, 34:]
        rd.astype(float)
    return (rd,faqui)

read_csv('cladding-FMC.txt')



import TFMimage
import TOF
import TOF2
import FMCdata
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


class TFM:
    def __init__(self,N,f0,faqui,rd,c2,pitch):
        self.N=N
        self.f0=f0
        self.faqui=faqui
        self.rd=rd
        self.c2=c2
        self.pitch=pitch

    def array_position(self):
        sarray = (self.N - 1) * self.pitch  # size of array
        self.xt = np.arange(-sarray / 2, sarray / 2 + self.pitch, self.pitch)  # 左开右闭原则，比matlab少一个元素所以再加一个pitch
        self.zt = np.zeros((self.N))

        return (self.xt, self.zt)

    def grid_position(self):
        self.XPmin = -0.025  #  minimal coordinate of x axis to focus
        self.XPmax = 0.025  #  maximal coordinate of x axis to focus
        self.ZPmin = 0  # minimal coordinate of z axis to focus
        self.ZPmax = 0.025  #  maximal coordinate of z axis to focus
        self.resolution = 0.0001  # 0.0001 m, grid resolution  (use 1/10(wavelenght)

        self.Gx = np.arange(self.XPmin, self.XPmax+self.resolution, self.resolution)
        self.Gz = np.arange(self.ZPmin, self.ZPmax+self.resolution, self.resolution)

        return (self.Gx, self.Gz, self.resolution)

    def grid_partition(self):
        self.grid_position()

        partes = 16  # number of blocks

        xsize = np.zeros((partes),dtype=int)
        xsize[:] = np.floor(self.Gx.shape[0] / partes)
        remainder = self.Gx.shape[0] % partes

        xsize=np.append(xsize,remainder)


        partes = xsize.size

        dimension = np.arange(1, partes+1)

        # return the coordinate of start and end point of each block, later used to
        self.xpmax = np.squeeze(self.XPmin - self.resolution + (xsize * self.resolution * dimension))
        self.xpmax[partes-1] = self.XPmax
        self.xpmin = self.xpmax - (xsize[:] - 1) * self.resolution

        #return the squence of start and end point of each block, later used in fill each block to I
        self.nxpmax = np.squeeze(xsize * dimension)
        self.nxpmax[partes-1] = np.sum(xsize)
        self.nxpmin = self.nxpmax - (xsize[:] - 1)

        self.partes = partes

        return (self.xpmin, self.xpmax, self.nxpmax, self.nxpmin, self.partes)

    def TFM_function(self):
        self.grid_partition()
        self.grid_position()
        self.array_position()

        FMCh = FMCdata.FMC(self.N, self.f0,self.faqui, self.rd)

        Gxsize = int(np.floor(self.Gx.size / self.partes))  # only integer can be used in np.empty

        I = np.zeros((self.Gx.size, self.Gz.size))  # create initial empty array for TFM

        for parte in range(self.partes - 1):
            temp = TOF.Time_of_flight(self.xpmin[parte], self.xpmax[parte], self.N, self.pitch, self.c2,
                                      self.ZPmin, self.ZPmax, self.resolution)

            Ip = TFMimage.amplitude(temp, self.faqui, FMCh, self.N)

            I[(self.nxpmin[parte] - 1):self.nxpmax[parte], :] = Ip


        temp2 = TOF2.Time_of_flight(self.xpmin[self.partes - 1], self.xpmax[self.partes - 1], self.ZPmin, self.ZPmax,
                                    self.N, self.pitch, self.c2)
        Ip2 = TFMimage.amplitude(temp2, self.faqui, FMCh, self.N)
        I[(self.nxpmin[self.partes-1] - 1):self.nxpmax[self.partes-1], :] = Ip2




        Iabs = np.abs(I)
        #Iabs4=Iabs/(np.max(Iabs))
        Iabs2 = Iabs.T
        Iab3 = np.fliplr(Iabs2)
        Iabs4 = Iab3 / (np.max(Iab3))

        im2 = plt.imshow(Iabs4, extent=[1000 * self.XPmin, 1000 * self.XPmax, 1000 * self.ZPmin, 1000 * self.ZPmax],)
                         #origin="lower")

        plt.colorbar(im2)
        plt.xlabel('Longitudinal position[mm]')
        plt.ylabel('Depth[mm]')
        plt.show()



import numpy as np
import warnings
warnings.filterwarnings('ignore')

rd,faqui=read_csv('cladding-FMC.txt')
trial= TFM(N=32,f0=5e6,faqui=faqui,rd=rd,c2=5950,pitch=0.001)

trial.TFM_function()




