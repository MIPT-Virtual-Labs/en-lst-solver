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
