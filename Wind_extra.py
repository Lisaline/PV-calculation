from datetime import timedelta
import math
import numpy as np

def W_ex(B,N_g,W,time,N,Pc,H,z):
    l=0
    r=0
    q=0
    tag=1
    P_bat=B*1000                         #Power needed for battery Wh
    N_g=N_g*1000
    i=0
    ws=list(range(26))
    P_wind=[]
    P_w=[]
    P_w_ex=[]
    
    
    while i < len(time):

        W2=W[i]*(math.log(H/z)/math.log(10/z))

        for a in ws:

            if W2<a+1 and W2>=a:
                                
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
    P_w_tot=sum(P_wind)  
    P_w_grid=sum(P_w_ex)             
        
    return  P_wind, P_w_ex,P_w_tot, P_w_grid