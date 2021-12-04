import numpy as np
import scipy.linalg as la
from blasius_problem import getMesh_U_DuDy, boundary_layer_thickness, get_y, get_U, get_dudy, get_h
from scipy.sparse.linalg import eigs
from pydantic import BaseModel, validator

# Functions to form matrix A and B from Spatial Eigenvalues problem Ax = alpha*Bx
def getE1():
    return np.array([[0, 0, 0],
                     [1, 0, 0],
                     [0, 1, 0]])

def getE2(Re):
    return np.array([[0, 1, 0],
                     [0, 0, 0],
                     [0, 0,-Re]])

def getE3(omega, Re, dudy):
    return np.array([[0, 0, 0],
                     [1j*omega*Re, -Re*dudy, 0],
                     [0, 1j*omega*Re, 0]])

def getInvE4(omega, Re, u):
    return la.inv(np.array([[-1j, 0, 0],
                       [1j*Re*u, 0, 1j*Re],
                       [0, 1j*Re*u, 0]]))

def getA_matrix(omega, Re, N, mesh, vels, grads, comp_num = 3):
    h = get_h(mesh)
    matrix_list = list()
    
    # Form first line of matrix A
    line = list()
    y = get_y(1, mesh)
    u = get_U(1, vels)
    dudy = get_dudy(1, grads)
    invE4 = getInvE4(omega, Re, u)
    E1 = invE4@getE1()
    E2 = invE4@getE2(Re)
    E3 = invE4@getE3(omega, Re, dudy)
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
        invE4 = getInvE4(omega, Re, u)
        E1 = invE4@getE1()
        E2 = invE4@getE2(Re)
        E3 = invE4@getE3(omega, Re, dudy)
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
    invE4 = getInvE4(omega, Re, u)
    E1 = invE4@getE1()
    E2 = invE4@getE2(Re)
    E3 = invE4@getE3(omega, Re, dudy)
    L1 = 1./h**2*E1 - 1./(2*h)*E2
    line.append(L1)
    L2 = E3 - 2./h**2*E1
    line.append(L2)
    matrix_list.append(line)

    return np.bmat(matrix_list)

class SS_InputParameters(BaseModel):
    N: int

    @validator("N")
    def check_N(cls, N):
        if N<200 or N>2000:
            raise ValueError("N is out of range! Correct range for N = [200, 2000]")
        return N

def spatial_solve(p: SS_InputParameters) -> np.ndarray:
    # mesh
    #N = 800
    N = p.N
    y_d, u_d, dudy_d = getMesh_U_DuDy(N, 15)
    
    # постановка задачи в размерных переменных
    mu = 1.85e-5
    rho = 1.214
    nu = mu/rho
    u_e = 50
    L = 3
    
    omega_d = 0.26/1.72
    Re_d = 1000/1.72
    x = nu/u_e*Re_d**2
    d = boundary_layer_thickness(nu, u_e, x)
    
    omega = omega_d*(u_e/d)
    Re = 1/nu
    
    y = y_d*d
    u = u_d*u_e
    dudy = dudy_d*u_e/d
    
    # расчет
    A = getA_matrix(omega, Re, N, y, u, dudy)
    eigvals, eigvec = eigs(A, 140, sigma=omega/u_e, which='LM')
    
    #обезразмерим alpha
    eigvals = eigvals*d
    return {"data" : eigvals}