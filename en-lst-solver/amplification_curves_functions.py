# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 12:51:02 2021

@author: mikhail
"""

import numpy as np
import scipy.linalg as la
from blasius_problem import getMesh_U_DuDy, getDimensionalMesh_U_DuDy, boundary_layer_thickness, getRe_d, get_y, get_U, get_dudy, get_h
from scipy.sparse.linalg import eigs
from progressbar import ProgressBar

# Functions to form matrix A and B from Spatial Eigenvalues problem Ax = alpha*Bx
def getE1():
    return np.array([[0, 0, 0],
                     [1, 0, 0],
                     [0, 1, 0]])

def getE2(nu):
    return np.array([[0, 1, 0],
                     [0, 0, 0],
                     [0, 0,-1/nu]])

def getE3(omega, nu, dudy):
    return np.array([[0, 0, 0],
                     [1j*omega/nu, -1/nu*dudy, 0],
                     [0, 1j*omega/nu, 0]])

def getInvE4(omega, nu, u):
    return la.inv(np.array([[-1j, 0, 0],
                       [1j/nu*u, 0, 1j/nu],
                       [0, 1j/nu*u, 0]]))

def getA_matrix(omega, nu, N, mesh, vels, grads, comp_num = 3):
    h = get_h(mesh)
    matrix_list = list()
    
    # Form first line of matrix A
    line = list()
    y = get_y(1, mesh)
    u = get_U(1, vels)
    dudy = get_dudy(1, grads)
    invE4 = getInvE4(omega, nu, u)
    E1 = invE4@getE1()
    E2 = invE4@getE2(nu)
    E3 = invE4@getE3(omega, nu, dudy)
    L2 = E3 - 2./h**2*E1
    line.append(L2)
    L3 = 1./h**2*E1 + 1./(2*h)*E2
    line.append(L3)
    for i in range(3,N):
        line.append(np.zeros((comp_num,comp_num)))
    matrix_list.append(line)

    # Form inner lines of matrix A
    for i in range(2, N-1):
        line = list()
        y = get_y(i, mesh)
        u = get_U(i, vels)
        dudy = get_dudy(i, grads)
        invE4 = getInvE4(omega, nu, u)
        E1 = invE4@getE1()
        E2 = invE4@getE2(nu)
        E3 = invE4@getE3(omega, nu, dudy)
        for j in range(1, N):
            if j==i-1:
                L1 = 1./h**2*E1 - 1./(2*h)*E2
                line.append(L1)
            elif j==i:
                L2 = E3 - 2./h**2*E1
                line.append(L2)
            elif j==i+1:
                L3 = 1./h**2*E1 + 1./(2*h)*E2
                line.append(L3)
            else:
                line.append(np.zeros((comp_num,comp_num)))
        matrix_list.append(line)

    # Form last line of matrix A
    line = list()
    for i in range(1, N-2):
        line.append(np.zeros((comp_num,comp_num)))
    
    y = get_y(N-1, mesh)
    u = get_U(N-1, vels)
    dudy = get_dudy(N-1, grads)
    invE4 = getInvE4(omega, nu, u)
    E1 = invE4@getE1()
    E2 = invE4@getE2(nu)
    E3 = invE4@getE3(omega, nu, dudy)
    L1 = 1./h**2*E1 - 1./(2*h)*E2
    line.append(L1)
    L2 = E3 - 2./h**2*E1
    line.append(L2)
    matrix_list.append(line)

    return np.bmat(matrix_list)


# get Tollmien–Schlichting wave from all modes
def getTSmode(eigvals, omega, u_e):
    ai_min = 0
    ar_min = 0
    for j in range(eigvals.size):
        ar = eigvals.real[j]
        ai = eigvals.imag[j]
        if  omega/u_e < ar and -150 < ai <= 0:
            if abs(ai) > abs(ai_min):
                ai_min = ai
                ar_min = ar
    return ai_min

# non-uniform on x direction
def get_y_by_eta(eta, L, g):
    return eta*L/(g - eta)

def get_g(y_e, L):
    return 1 + L/y_e

# for calculation of amplification curves    
def Nfactor(x, ai):
    Nom = np.zeros(x.size)
    h = x[0]
    Nom[0] = -h/2*(ai[0])
    for i in range(1, x.size):
        h = x[i] - x[i-1]
        Nom[i] = Nom[i-1] - h/2*(ai[i] + ai[i-1])
    return Nom

def amplfication_curves_solve(omega_min, omega_max, number_of_omegas):
    # mesh
    #N = 800
    if omega_min<500 or omega_max>10000 or number_of_omegas<1 or number_of_omegas>8 or omega_max<omega_min:
        if number_of_omegas<1 or number_of_omegas>7:
            print("Number of omegas is out of range. Must be in [1,8]")
        if omega_min<500:
            print("Omega_min is too low! Minimal value is 500")
        if omega_max>10000:
            print("Omega_max is too high! Maximal value is 10000")
        if omega_max<omega_min:
            print("Omega_max < Omega_min! Omega_min must be less Omega_max")
        return np.zeros(N)
    else:
        mu = 1.85e-5
        rho = 1.214
        nu = mu/rho
        u_e = 50
        N = 2000
        y_d, u_d, dudy_d = getMesh_U_DuDy(N, 10)
        L = 1.5
        eta = np.linspace(0, 1, 20)
        g = get_g(3, L)
        
        pbar_omega = ProgressBar()
        #x_mesh = np.linspace(0.05, 3, 10)
        x_mesh = get_y_by_eta(eta, L, g)
        x_mesh = x_mesh[1:]
        #omega_mesh = np.linspace(1000, 7000, 20)
        omega_mesh = np.linspace(omega_min, omega_max, number_of_omegas)
        ai_for_omega = []
        amplification_curves = []
        for omega in pbar_omega(omega_mesh):
            ai_s = []
            for x in x_mesh:
                y, u, dudy = getDimensionalMesh_U_DuDy(x, u_e, nu, y_d, u_d, dudy_d)
                A = getA_matrix(omega, nu, N, y, u, dudy)
                eigvals, eigvec = eigs(A, 100, sigma=2*omega/u_e, which='LM')
                ai = getTSmode(eigvals, omega, u_e)
                ai_s.append(ai)
            ai_for_omega.append(ai_s)
            amplification_curves.append(Nfactor(x_mesh, ai_s))
            
        return x_mesh, ai_for_omega, amplification_curves
    
    
    
    
    
    
    
    
    
    
    
    
    