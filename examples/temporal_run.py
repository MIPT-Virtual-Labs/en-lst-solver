# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 15:16:52 2021

@author: mikhail
"""
import sys
sys.path.insert(1, '../en-lst-solver')

import argparse
import matplotlib.pyplot as plt
from temporal_functions import temporal_solve

def main(Re, alpha):
    eigvals = temporal_solve(Re, alpha)
    plt.plot(eigvals.real, eigvals.imag, '+b', label='Numerical')
    plt.legend()
    plt.xlim(0, 1)
    plt.ylim(-1, 0.1)
    plt.grid() 
    plt.xlabel('c_re')
    plt.ylabel('c_im')
    plt.savefig('Temporal spectrum.jpg')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="values of Re an alpha")
    parser.add_argument("Re", help="Reynolds number", type=int)
    parser.add_argument("alpha", help="wave number alpha", type=float)
    args = parser.parse_args()
    Re = args.Re
    alpha = args.alpha
    main(Re, alpha)