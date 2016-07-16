# -*- coding: utf-8 -*-
"""

This program calculates impact velocity and times for forward/reverse motion
based on formulae derived from the equations of motion, for each contact. 

@author: Ashwin Ramakrishnan
"""
from pylab import *

#main function
if __name__=='__main__':
    
    #Collecting user inputs
    Mag = float(raw_input("Enter the value of M in A/m: "))
    delB= float(raw_input("Enter the value of delB in T/m: "))
    r = float(raw_input("Enter the value of radius in meters: "))
    L = float(raw_input("Enter the value of Length of tube in meters: "))
    k = float(raw_input("Enter the value of k in N/m: "))
    e = float(raw_input("Enter the value of CoeR: "))
    
    den = float(raw_input("Enter the value of density in kg/m3: "))
    
    v = 4*pi*(r**3)/3 #Volume of ball
    m = den * v #Mass of ball
    Fb = v*delB*Mag #Force on ball
    w = sqrt(k/m)
    
    a = Fb/m #Acceleration on ball
    NoC = range(1,101) #100 contacts
    
    V0 = 0
    sum = 0
    
    trev1=0
    trev2=0
    tfor1=0
    tfor2=0
    tsum1 = 0
    tsum2 = 0
    
    Vimplist = list() #List to store impact velocities
    ttotlist = list() #list to store total time for each contact
    t_transitionlist = list() #list to store times at which gradient signal switches
    
    #Following loop calculates impact velocity for each contact
    for i in NoC: 
        Vimp1 = sqrt(V0**2+(2*a*L)) 
        tfor2 = (Vimp1-V0)/a 
        tsum1 = tsum2+(tfor1+tfor2)
        
        t_transitionlist.append(round(tsum1,4))
        
        Vimplist.append(Vimp1)
        sum = sum + Vimp1
        
        ttot = trev1+trev2+tfor1+tfor2
        ttotlist.append(ttot)
                     
        V2 = e*Vimp1
        V3 = sqrt(V2**2+(2*a*L))
        trev1 = (V3 - V2)/a
        
        y0 = (Fb + sqrt(Fb**2+(k*m*V3**2)))/k
        
        for n in range(-10,10):
            trev2 = ((pi*n)-arctan((k*V3)/(Fb*w)))/w #Time for ball to move from y=0 to y=y0 i.e. full spring compression
            if trev2 > 0:
                break
        tsum2 = tsum1+(trev1+trev2)
        t_transitionlist.append(round(tsum2,4))
                
        for n in range(-10,10):    
            tfor1 = (arccos(Fb/(Fb+k*y0))+(2*pi*n))/w #Time for ball to move from y=y0 to y=0 after full spring compression
            if tfor1>0:
                break
        
        V4 = sqrt(((k/m)*y0**2)+(2*Fb*y0/m))
        V0 = V4
    
    print 'Average impact velocity over 100 contacts =', round(sum/100,4)
    
    tfinal = tsum2
    timerange = arange(0,round(tsum2,4),0.0001)  
    Blist=list()
    
    #Following loop stores values of delB w.r.t time for the required i/p wave
    for j in timerange: 
        j=round(j,4)
        if j in t_transitionlist:
            if t_transitionlist.index(j)%2==0:                                
                delB = -delB
                Blist.append(delB)
                continue
            else:             
                delB = delB
                Blist.append(delB)     
                continue
        Blist.append(delB)
    
    #Plotting Impact velocity vs. no. of contacts
    figure(0)    
    plot(NoC, Vimplist, linewidth = 2.0)
    xlabel('No. of contacts')
    ylabel('Impact velocity (m/s)')
    grid(True)
    show()
    
    #Plotting Total time for each impact vs. no. of contacts
    figure(1)
    plot(NoC, ttotlist, linewidth = 2.0)
    xlabel('No. of contacts')
    ylabel('Time b/w impacts (s)')
    grid(True)
    show()       
    
    #Plotting the required i/p gradient wave (delB vs. t)
    figure(2)
    plot(timerange, Blist, linewidth = 2.0)
    xlabel('Time (s)')
    ylabel('delB (T/m)')
    grid(True)
    show()       
    
