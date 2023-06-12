from datetime import timedelta
import math
import numpy as np



def E_ex(breite,länge,G,time,H_sun,P_bat,eta,tilt, orientation,A):

    '''____________________________________Suns azimut_______________________________________'''
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
    l=0
    r=0
    tag=1
    P_out=[]
    i=0
    q=0
    P_ex=[]
    P_ov=[]
    P_tot=0
    ws=[2.5,3,4,5,6,7,8,9,10,11,12,13,14,15]
    Pc=[100,200,500,900,1400,2200,3500,5000,6500,7500,8500,8500,8500,8500] #Data from https://www.braun-windturbinen.com/produkte/antaris-kleinwindanlagen/antaris-7-5-kw/
    P_wind=0
    P_w=[]
    P_top=[]

    '''_________________Calculation of needed PV area for an average year_______________________''' 
        

    while i < len(time):
                    
        h_run=time[i]

        if G[i]<=0:
            P_out.append(0)
                    
        else:
            if G [i] > 1367:                                   #if radiation over extraterrestrial radiation
                G[i] = 1367
                            
            f = (math.cos(tilt*math.pi/180)*math.cos((90 - H_sun[i])* math.pi/180) + math.sin(tilt* math.pi/180)*math.cos((90- H_sun[i])* math.pi/180)*math.cos((so(H_sun[i],breite,länge,tag,h_run)-orientation)* math.pi/180))/math.cos((90-H_sun[i])* math.pi/180)
            if f<0:
                f=0
                        
            P_out.append(eta*f*G[i]*A)        #Wh

        
        l+=1
        i+=1
                    
                    
        if l==24:
            P_ex.append(sum(P_out)) 
            
            
            if sum(P_out)<=P_bat: 
                P_ov.append(sum(P_out)-P_bat)
            else:
                P_ov.append(0)
                P_tot+=(sum(P_out)-P_bat)
            l=0
            P_out.clear()
            P_w.clear()        
        #if l==24:
            #r+=1
            #P_sum=sum(P_out)                          #Power output of PV in one day Wh
                        
            #if P_sum>=P_bat:
                #P_ex.append(P_sum)                #excess power 
                #tag+=1
                #r=0
                            
            #else:
                #if r<2:
                    #tag+=1
                        
                #if r==2:
                    #A+=1
                    #i-=48
                    #tag-=2
                    #r=0
                        

            #P_sum=0
        
            #l=0
    P_grid=sum(P_ov)
    
    return P_ex, P_ov, P_grid, P_tot