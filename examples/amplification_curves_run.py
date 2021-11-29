# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 15:16:43 2021

@author: mikhail
"""

import sys
sys.path.insert(1, '../en-lst-solver')

import argparse
import matplotlib.pyplot as plt
from amplification_curves_functions import amplfication_curves_solve
import numpy as np

def main(omega_min, omega_max, number_of_omegas):
    x_mesh, ai_for_omega, amplification_curves = amplfication_curves_solve(omega_min, omega_max, number_of_omegas)
    omega_mesh = np.linspace(omega_min, omega_max, number_of_omegas)
    
    #plot unstable modes
    for i in range(number_of_omegas):
        text = str(omega_mesh[i])
        plt.plot(x_mesh, ai_for_omega[i], label = text) 
    plt.savefig('../out/Unstable modes.jpg')
    plt.clf()
    
    #plot amplification curves
    for i in range(number_of_omegas):
        plt.plot(x_mesh, amplification_curves[i])
    
    plt.plot(0.784, 7.82, 'ro', label = 'Tu= 0,12 %')
    plt.plot(1.25, 10.7, 'ro')
    plt.plot(0.597, 6.45, 'bo',  label = 'Tu= 0,2 %')
    plt.plot(1.02, 9.32, 'bo')
    plt.ylim(0, 18)
    plt.legend()
    name = 'Расчет положений ЛТП'
    plt.title(name)
    plt.savefig('../out/Amplification_curves.jpg')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="general parameters")
    parser.add_argument("omega_min", help="Minimal omega", type=int)
    parser.add_argument("omega_max", help="Maximal omega", type=int)
    parser.add_argument("number_of_omegas", help="Number of omegas", type=int)
    args = parser.parse_args()
    omega_min = args.omega_min
    omega_max = args.omega_max
    number_of_omegas = args.number_of_omegas
    main(omega_min, omega_max, number_of_omegas)
    
    
    
    
    
    
    