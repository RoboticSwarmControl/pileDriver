# -*- coding: utf-8 -*-
"""

This program calculates impact velocity based on formulae derived from 
the equations of motion, for each contact.

@author: Ashwin Ramakrishnan
"""
from pylab import *

#main function
if __name__=='__main__':
    
    #Collecting user inputs
    Mag = float(raw_input("Enter the value of M in A/m: "))
    
    delB= float(raw_input("Enter the value of delB in T/m: "))
    r = float(raw_input("Enter the value of r in meters: "))
    L = float(raw_input("Enter the value of L in meters: "))
    k = float(raw_input("Enter the value of k in N/m: "))
    e = float(raw_input("Enter the value of CoeR: "))
    
    den = float(raw_input("Enter the value of density in kg/m3: "))
    
    v = 4*pi*(r**3)/3 #Volume of ball
    m = den * v #Mass of ball
    Fb = v*delB*Mag #Force on ball
    
    a = Fb/m #Acceleration on ball
    NoC = range(1,101) #100 contacts
    
    V0 = 0
    sum = 0
    
    Vimplist = list() #List to store impact velocities
    
    #Following loop calculates impact velocity for each contact
    for i in NoC: 
        Vimp1 = sqrt(V0**2+(2*a*L))
        Vimplist.append(Vimp1)
        sum = sum + Vimp1
        print 'Impact velocity #', i,'=',Vimp1
        
        V2 = e*Vimp1
        V3 = sqrt(V2**2+(2*a*L))
      
        
        y0 = (Fb + sqrt(Fb**2+(k*m*V3**2)))/k
   
        
        V4 = sqrt(((k/m)*y0**2)+(2*Fb*y0/m))
        V5 = sqrt(V4**2+(2*a*L))
        V0 = V4
    
    print 'Average impact velocity over 100 contacts =', sum/100
    
    #Plotting Impact velocity vs. no. of contacts
    plot(NoC, Vimplist, linewidth = 2.0)
    xlabel('Impact velocity (m/s)')
    ylabel('No. of contacts')
    grid(True)
    show()
    
            
    
