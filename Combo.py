import math
from datetime import timedelta
import math
import numpy as np
import Excess_electricity as Exe
import Wind_extra as Wex

class combo():

    def __init__ (self,breitengrad,längengrad,G,time,H_sun,T2m,E,eta, N_g ,W,WT,Pc,H,An):
        self.breite = breitengrad
        self.länge = längengrad
        self.G = G
        self.time = time
        self.H_sun = H_sun
        self.T2m = T2m
        self.B = E
        self.eta=eta
        self.N_g=N_g
        self.W= W
        self.WT=WT
        self.Pc=Pc
        self.H=H
        self.An=An
    
    def Combo(self):
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
        P_w_out=[]
        breaker=False
        
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

                        if N >= self.An:
                            breaker= True
                            break
                P_wind=0
                P_w.clear()
                l=0
                p=0
                    
            if breaker:
                break
                


               
        
        P_w_out,P_w_ex, P_w_tot, P_w_grid= Wex.W_ex(self.B,self.N_g,self.W,self.time,N,self.Pc,self.H,z)
        




        if any(x<P_bat for x in P_w_out):

            def so(H,breite,länge,tag,time):
        
                roh = 0.409*math.sin((2*math.pi*tag/365) -1.39)     #Sundeclination in rad
                i,d= math.modf((länge/15))
                
                if breite <0:
                    if roh >= breite:

                        try:
                            if (time.hour + d+i*60*10**(-2))> 12:                                  #UTC into local time
                                az = -math.acos((math.sin(H* math.pi/180)*math.sin(breite* math.pi/180) - math.sin(roh))/(math.cos(H* math.pi/180)*math.cos(breite* math.pi/180)))*180/math.pi
                            else:
                                az = math.acos((math.sin(H* math.pi/180)*math.sin(breite* math.pi/180) - math.sin(roh))/(math.cos(H* math.pi/180)*math.cos(breite* math.pi/180)))*180/math.pi
                        except ValueError:        
                            az = 180
                    
                    else:
                        try:
                            if (time.hour + d+i*60*10**(-2))> 12:                                  #UTC into local time
                                az = -math.acos((math.sin(H* math.pi/180)*math.sin(-breite* math.pi/180) - math.sin(roh))/(math.cos(H* math.pi/180)*math.cos(-breite* math.pi/180)))*180/math.pi
                            else:
                                az = math.acos((math.sin(H* math.pi/180)*math.sin(-breite* math.pi/180) - math.sin(roh))/(math.cos(H* math.pi/180)*math.cos(-breite* math.pi/180)))*180/math.pi
                        except ValueError:        
                            az = 0
    
                else:
                    if roh >= breite:

                        try:
                            if (time.hour + d+i*60*10**(-2))> 12:                                  #UTC into local time
                                az = -math.acos((math.sin(H* math.pi/180)*math.sin(-breite* math.pi/180) - math.sin(roh))/(math.cos(H* math.pi/180)*math.cos(-breite* math.pi/180)))*180/math.pi
                            else:
                                az = math.acos((math.sin(H* math.pi/180)*math.sin(-breite* math.pi/180) - math.sin(roh))/(math.cos(H* math.pi/180)*math.cos(-breite* math.pi/180)))*180/math.pi
                        except ValueError:        
                            az = 180
                    
                    else:
                        try:
                            if (time.hour + d+i*60*10**(-2))> 12:                                  #UTC into local time
                                az = -math.acos((math.sin(H* math.pi/180)*math.sin(breite* math.pi/180) - math.sin(roh))/(math.cos(H* math.pi/180)*math.cos(breite* math.pi/180)))*180/math.pi
                            else:
                                az = math.acos((math.sin(H* math.pi/180)*math.sin(breite* math.pi/180) - math.sin(roh))/(math.cos(H* math.pi/180)*math.cos(breite* math.pi/180)))*180/math.pi
                        except ValueError:        
                            az = 0
                
                return az

            
            #constants

            phi = [90,45,15,0,-15,-45,-90]                                    #Modul orientation east to west         
            beta=[0,15,30,45,60,75,90]                                        #Modul tilt
            area=np.zeros(shape=(7,7))
            l=0
            m=0
            o=0
            r=0
            s=0
            p=0
            tag=1
            P_out=[]
            B=1
            i=0
            

            '''_________________Calculation of needed PV area for an average year_______________________''' 
            for x in phi:

                for y in beta:

                    while i < len(self.time):
                        
                        h_run=self.time[i]

                        if self.G[i]<=0:
                            P_out.append(0)
                        
                        else:
                            if self.G [i] > 1367:                                   #if radiation over extraterrestrial radiation
                                self.G[i] = 1367
                                
                            f = (math.cos(y*math.pi/180)*math.cos((90 - self.H_sun[i])* math.pi/180) + math.sin(y* math.pi/180)*math.cos((90- self.H_sun[i])* math.pi/180)*math.cos((so(self.H_sun[i],self.breite,self.länge,tag,h_run)-x)* math.pi/180))/math.cos((90-self.H_sun[i])* math.pi/180)
                            if f<0:
                                f=0
                            
                            P_out.append(self.eta*f*self.G[i]*B)        #Wh

                        l+=1
                        i+=1
                        
                        
                        
                        if l==24:
                            r+=1
                            P_sum=sum(P_out)                          #Power output of PV in one day Wh
                            
                            for p in range(101):
                                
                                if P_sum + P_w_out[s]>=(P_bat-(p/100)*self.N_g): 
                                    tag+=1
                                    r=0 
                                    s+=1
                                    
                                    break
                                
                                if p==100:
                                    
                                    if r<2:
                                        tag+=1
                                        s+=1
                                    if r==2:
                                        B+=1
                                        i-=48
                                        tag-=2
                                        r=0
                                        s-=2
    
                            p=0
                            P_sum=0
                            P_out.clear()
                            l=0
                            s=0
                            
                    
                    
                    '''_________________Finding best orientation and tilt angles_______________________''' 
                    
                    fläche_flach= np.ravel(area)
                    fläche_flach = np.ma.masked_equal(area,0)
                    
                    
                    if (fläche_flach > B).all():
                        tilt =y
                        orientation =x
                        A_best=B
                    area[m,o]=B
                    i=0
                    m+=1  
                    B=1
                    tag=1
                    r=0
                m=0
                o+=1
            P_ex, P_ov,P_grid, P_tot =Exe.E_ex(self.breite,self.länge,self.G,self.time,self.H_sun,P_bat,self.eta,tilt,orientation,A_best,P_w_out)
            
            C=len(P_ex)
            
            return area, beta, phi, tilt, orientation,P_ex, C, P_ov,P_grid,P_tot, P_w_out, 1, N

        else:
            return 2

