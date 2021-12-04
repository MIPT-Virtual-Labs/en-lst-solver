# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 15:16:52 2021

@author: mikhail
"""
import sys
sys.path.insert(1, '../en-lst-solver')

import matplotlib.pyplot as plt
from handle_request import handle_request

def main(request):
    response_dict = handle_request(request)
    eigvals = response_dict['solution']['data']
    
    plt.plot(eigvals.real, eigvals.imag, '+b', label='Numerical')
    plt.legend()
    plt.xlim(0, 1)
    plt.ylim(-1, 0.1)
    plt.grid() 
    plt.xlabel('c_re')
    plt.ylabel('c_im')
    plt.savefig('../out/Temporal spectrum.jpg')

if __name__ == "__main__":
    params = dict(alpha=1, Re=10000)
    request = dict(problem="TS", args=params)
    main(request)
    
    
    
    
    
    
    
    
    
    