# -*- coding: utf-8 -*-
"""
This program calculates the resonant impact velocity and forward time, reverse time
for the input gradient wave, based on user inputs. All formulae have been derived 
analytically on the premise that at resonance/steady state, the impact velocity remains
constant over successive contacts.

@author: Ashwin Ramakrishnan
"""
from pylab import *


#main function
if __name__=='__main__':
    
    #Accepting user inputs   
    
    Mag = float(raw_input("Enter the value of M in A/m: "))
    
    delB= float(raw_input("Enter the value of delB in T/m: "))
    r = float(raw_input("Enter the value of r in meters: "))
    L = float(raw_input("Enter the value of L in meters: "))
    k = float(raw_input("Enter the value of k in N/m: "))
    e = float(raw_input("Enter the value of CoeR: "))
    
    den = float(raw_input("Enter the value of density in kg/m3: "))
    v = 4*pi*(r**3)/3 #Volume of a spherical ball
       
    m = den * v #Mass of ball
    f = v*delB*Mag #Force on ball
    
    a = f/m #Acceleration on ball
    w = sqrt(k/m) #Natural frequency of spring-mass system
    vimp = 0    
     
    #Calculating resonant impact velocity based on derived analytical formula 
    vimp_1 = 2/(1-e**2)
    vimp_2 = sqrt((Mag*delB*1.33*pi*r**3)**2*(1+e**2)**2+2*(Mag*delB*1.33*pi*r**3)*k*L*(1-e**4))
    vimp_3 = sqrt((Mag*delB/(k*den))*(1.33*pi*delB*Mag*r**3*(e**2+1)-k*L*(e**2-1)+vimp_2))
    
    vimp = vimp_1*vimp_3
    
    print '\nSteady state/resonant velocity =', vimp,'m/s'
    
    v2 = sqrt((e**2*vimp**2)+2*a*L) #Velocity at y=0 when ball moves from y=L in reverse dirn. after impact 
    
    t1 = (v2-e*vimp)/a #Time for ball to move from y=L to y=0 at resonance/steady state
               
    for n in range(-10,10):
        t2 = ((pi*n)-arctan((k*v2)/(f*w)))/w #Time for ball to move from y=0 to y=y0 i.e. full spring compression
        if t2 > 0:
            break
    
    trev = t1 + t2 #Total time in reverse direction i.e. Forceonball is negative for this duration

    y0 = (f + sqrt(f**2+(k*m*e**2*vimp**2)+(2*k*f*L)))/k #Distance of max. spring compression from y=0
        
    for n in range(-10,10):    
        t3 = (arccos(f/(f+k*y0))+(2*pi*n))/w #Time for ball to move from y=y0 to y=0 after full spring compression
        if t3>0:
            break

    v3 = sqrt(vimp**2-2*a*L) #Velocity at y=0 after full spring compression
    t4 = (vimp - v3)/a #Time for ball to move from y=0 to y=L in the forward direction
        
    tfor = t3+t4 #Total time in forward direction i.e. Forceonball is positive for this duration
    
            
    print '\nDuration for which Forceonball is negative, trev =',trev,"s"
    print '\nDuration for which Forceonball is positive, tfor =',tfor,"s"
    print '\nTotal time between 2 impacts at resonance/steady state, ttot =', trev +tfor,'s'  
    
