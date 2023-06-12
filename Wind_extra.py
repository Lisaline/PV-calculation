from datetime import timedelta
import math
import numpy as np

def W_ex(B,N_g,W,time,N):
    l=0
    r=0
    q=0
    tag=1
    P_bat=B*1000                         #Power needed for battery Wh
    N_g=N_g*1000
    i=0
    ws=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    Pc=[0,0,100,200,500,900,1400,2200,3500,5000,6500,7500,8500,8500,8500,8500] #Data from https://www.braun-windturbinen.com/produkte/antaris-kleinwindanlagen/antaris-7-5-kw/
    P_wind=[]
    P_w=[]
    P_w_ex=[]

    
    while i < len(time):
                
        for a in ws:

            if W[i]<a+1 and W[i]>=a:
                                
                P_w.append(Pc[q]*N)
            q+=1
        l+=1
        q=0
        i+=1
        if l==24:
            P_wind.append(sum(P_w))

            if sum(P_w) < P_bat:
                P_w_ex.append(sum(P_w)-P_bat)
            
            else:
                P_w_ex.append(0)
            
            
            P_w.clear()
            l=0
                    
        
    return  P_wind, P_w_ex