from temporal_functions import *

N = 300
# test 1
alpha = 1
Re = 10000
A = getA_matrix(alpha, Re, N)
B = getB_matrix(alpha, Re, N)

import scipy.linalg as la
eigvals = la.eigvals(A, B)
eigvals = eigvals/alpha

import matplotlib.pyplot as plt

plt.plot(eigvals.real, eigvals.imag, '+b', label='Numerical')
plt.legend()
# test 1
plt.xlim(0, 1)
plt.ylim(-1, 0.1)
plt.grid() 
plt.xlabel('c_re')
plt.ylabel('c_im')
plt.savefig('Temporal spectrum.jpg')