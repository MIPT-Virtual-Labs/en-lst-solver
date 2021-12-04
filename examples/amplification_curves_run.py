# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 15:16:43 2021

@author: mikhail
"""

import sys
sys.path.insert(1, '../en-lst-solver')

import matplotlib.pyplot as plt
from handle_request import handle_request
import numpy as np
from amplification_curves_functions import ACS_InputParameters

def main(request):
    response_dict = handle_request(request)
    x_mesh = response_dict['solution']['x_mesh']
    ai_for_omega = response_dict['solution']['ai_for_omega']
    amplification_curves = response_dict['solution']['amplification_curves']
    
    p = ACS_InputParameters(**request['args'])
    omega_min = p.omega_min
    omega_max = p.omega_max
    number_of_omegas = p.number_of_omegas
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
    params = dict(omega_min=1000, omega_max=7000, number_of_omegas=8)
    request = dict(problem="ACS", args=params)
    main(request)
    
    
    
    
    
    
    