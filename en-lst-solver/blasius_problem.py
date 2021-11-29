# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 17:20:48 2021

@author: mikhail
"""

import scipy.integrate as scii
import numpy as np


def rhs(f, t):
    return np.array([f[1], f[2], -0.5*f[0]*f[2]])

#blasius profile
def getMesh_U_DuDy(N, y_max):
    x = np.linspace(0, y_max, N+1)
    y = scii.odeint(rhs, np.array([0, 0, 1]), x)
    a = 1/(y[-1,1])**0.5
    x = x/a
    y[:, 0] = y[:, 0]*a
    y[:, 1] = y[:, 1]*a**2
    y[:, 2] = y[:, 2]*a**3
    return x, y[:, 1], y[:,2]

def boundary_layer_thickness(nu, u_e, x):
    return (nu*x/u_e)**0.5

def getDimensionalMesh_U_DuDy(x, u_e, nu, y_d, u_d, dudy_d):
    d = boundary_layer_thickness(nu, u_e, x)
    y = y_d*d
    u = u_d*u_e
    dudy = dudy_d*u_e/d
    return y, u, dudy

def getRe_d(nu, u_e, d):
    return u_e*d/nu

def get_y(j, y):
    return y[j]

def get_U(j, vels):
    return vels[j]

def get_dudy(j, grads):
    return grads[j]

def get_h(y):
    return y[1] - y[0]