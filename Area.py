from datetime import timedelta
import math
import numpy as np
import Excess_electricity as Exe




class calculation():

    def __init__(self,breite,länge,G,time,H_sun,T2m,B,eta,N_g):
        self.breite = breite
        self.länge = länge
        self.G = G
        self.time = time
        self.H_sun = H_sun
        self.T2m = T2m
        self.B = B
        self.eta=eta
        self.N_g=N_g
        


    def PV(self):

        '''____________________________________Suns azimut_______________________________________'''
        def so(H,breite,länge,tag,time):
    
            roh = 0.409*math.sin((2*math.pi*tag/365) -1.39)     #Sundeclination [rad]
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

        phi = [90,45,15,0,-15,-45,-90]                                    #Modul orientation east to west [°]         
        beta=[0,15,30,45,60,75,90]                                        #Modul tilt [°]
        area=np.zeros(shape=(7,7))
        l=0
        m=0
        o=0
        r=0
        tag=1
        P_out=[]
        A=1
        P_bat=self.B*1000                                                 #Power needed for battery [Wh]
        self.N_g=self.N_g*1000
        i=0
        P_w_out=[0]*380
        
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
                        
                        P_out.append(self.eta*f*self.G[i]*A)        #[Wh]

                    l+=1
                    i+=1
                    
                    
                    
                    if l==24:
                        r+=1
                        P_sum=sum(P_out)                          #Power output of PV in one day [Wh]
                        
                        for p in range(101):
                            
                            if P_sum>=(P_bat-(p/100)*self.N_g): 
                                tag+=1
                                r=0 
                                
                                break
                            
                            if p==100:
                                
                                if r<2:
                                    tag+=1
                        
                                if r==2:
                                    A+=1
                                    i-=48
                                    tag-=2
                                    r=0
                        p=0
                        P_sum=0
                        P_out.clear()
                        l=0
                        
                    
                
                '''_________________Finding best orientation and tilt angles_______________________''' 
                
                fläche_flach= np.ravel(area)
                fläche_flach = np.ma.masked_equal(area,0)
                
                
                if (fläche_flach > A).all():
                    tilt =y
                    orientation =x
                    A_best=A
                area[m,o]=A
                i=0
                m+=1  
                A=1
                tag=1
                r=0
            
            m=0
            o+=1
        P_ex, P_ov,P_grid, P_tot =Exe.E_ex(self.breite,self.länge,self.G,self.time,self.H_sun,P_bat,self.eta,tilt,orientation,A_best,P_w_out)
        N=len(P_ex)
       
        return area, beta, phi, tilt, orientation,P_ex,N, P_ov,P_grid,P_tot