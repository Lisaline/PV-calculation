from datetime import timedelta
import math
import numpy as np
import Wind_extra as Wex




class wind():

    def __init__(self,B,N_g,W,WT,time):
        
        self.B = B
        self.N_g=N_g
        self.W= W
        self.WT=WT
        self.time=time

    def Wind(self):

        #constants
        l=0
        r=0
        q=0
        N=1
        P_bat=self.B*1000                         #Power needed for battery Wh
        self.N_g=self.N_g*1000
        i=0
        ws=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        Pc=[0,0,100,200,500,900,1400,2200,3500,5000,6500,7500,8500,8500,8500,8500] #Data from https://www.braun-windturbinen.com/produkte/antaris-kleinwindanlagen/antaris-7-5-kw/
        P_wind=0
        P_w=[]

        while i < len(self.time):
            
            if self.WT==1:
                
                for a in ws:

                    if self.W[i]<a+1 and self.W[i]>=a:
                                
                        P_w.append(Pc[q]*N)
                    q+=1
                l+=1
                q=0
                i+=1
                if l==24:
                    r+=1
                    P_wind=sum(P_w)

                    for p in range(101):
                            
                        if P_wind>=(P_bat-(p/100)*self.N_g): 
                            r=0 
                                
                            break
                            
                        if p==100:
                        
                            if r==2:
                                N+=1
                                i-=48
                                r=0
  
                    
                    P_wind=0
                    P_w.clear()
                    l=0
                    p=0
                    
        P_w_out , P_w_ex = Wex.W_ex(self.B,self.N_g,self.W,self.time,N)
        
        return  N, P_w_out,P_w_ex       
