# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 17:31:24 2021

@author: mikhail
"""

import sys
sys.path.insert(1, '../en-lst-solver')

import argparse
import matplotlib.pyplot as plt
from spatial_functions import spatial_solve
import numpy as np

def main(N):
    eigvals = spatial_solve(N)
    
    paper_data = np.array([[0.2600153645394847,0.005216576864792044],
                           [0.2649509597575349,0.04520717573104338],
                           [0.267293525846102,0.08786938036706515],
                           [0.2709547061794915,0.12519574002357303],
                           [0.2732972722680586,0.1678579446595948],
                           [0.27947781613066175,0.2158461721950946],
                           [0.28170988381882467,0.27850858730426],
                           [0.28521636639164843,0.3438352416231689],
                           [0.28491433743054384,0.3985024835830948],
                           [0.28456810910927766,0.46116980973227817],
                           [0.28552576191277995,0.5211679856317001],
                           [0.29872663748105743,0.23180950777347475],
                           [0.5419115170904193,0.08201296514564738],
                           [0.7428786411853847,0.3402968372902284],
                           [0.28653498063647076,0.5718327299769883]])
    
    paper_data /= 1.72
    
    plt.plot(paper_data[:,0], paper_data[:,1], 'xr', label='Paper') # test case for omega = 0.26
    plt.plot(eigvals.real, eigvals.imag, '+b', label='Numerical, N='+str(N))
    plt.legend()
    plt.xlim(0.1, 0.5)
    plt.ylim(-0.1, 0.3)
    plt.grid() 
    plt.xlabel('a_re')
    plt.ylabel('a_im')
    plt.savefig('../out/Spatial spectrum.png')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="value of N")
    parser.add_argument("N", help="number of nodes", type=int)
    args = parser.parse_args()
    N = args.N
    main(N)