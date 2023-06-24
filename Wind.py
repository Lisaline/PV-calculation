from datetime import timedelta
import math
import numpy as np
import Wind_extra as Wex




class wind():

    def __init__(self,B,N_g,W,WT,time,Pc,H):
        
        self.B = B
        self.N_g=N_g
        self.W= W
        self.WT=WT
        self.time=time
        self.Pc=Pc
        self.H=H

    def Wind(self):

        #constants
        l=0
        r=0
        q=0
        N=1
        i=0
        z=0.8                                     #roughness length
        P_bat=self.B*1000                         #Power needed for battery Wh
        self.N_g=self.N_g*1000
        ws=list(range(26))
        P_wind=0
        P_w=[]


        while i < len(self.time):
            
            W2=self.W[i]*(math.log(self.H/z)/math.log(10/z))   
            for a in ws:
                
                if W2<a+1 and W2>=a:
                                
                    P_w.append(self.Pc[q]*N)
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
                    
        P_w_out , P_w_ex = Wex.W_ex(self.B,self.N_g,self.W,self.time,N,self.Pc,self.H,z)
        
        return  N, P_w_out,P_w_ex       
