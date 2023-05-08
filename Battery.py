from datetime import timedelta
import math
import numpy as np

class battery():
    def __init__(self,N_c,N_g,N_t):
        self.N_c=N_c
        self.N_g=N_g
        self.N_t=N_t


    def Bat(self):

        #constants

        a=0.6               #charging from 20-80%
        b=0.1               #losses from converter...
        c=2                 #number of charging cycles
        d=0.1               #safety marging in batteries
        e=2980              #battery capacity with 80% DOD
        A=14.915            #surface area of one battery house

        '''_________________Calculating energy needed to charge trucks and battery size_______________________''' 

        E=self.N_c*self.N_t*a  #*(1-self.N_g)      #total energy needed from BESS to charge trucks [kWh]
        C=(E*(1+b)*c)*(1+d)                     #needed energy storage capacity [kWh]
        N_u=round(C/e,0)                        #number of battery units
        N_a=N_u*A                               #total surface area [m^2]

        return E, C, N_u, N_a