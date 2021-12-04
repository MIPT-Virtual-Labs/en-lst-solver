from scipy.sparse import block_diag
import numpy as np
from channel_flow_problem import *
import scipy.linalg as la
from pydantic import BaseModel, validator

def getE1(Re):
    return np.array([[1/Re, 0, 0],
                     [0, 1/Re, 0],
                     [0, 0, 0]])

def getE2():
    return np.array([[0, 0, 0],
                     [0, 0, -1],
                     [0, 1, 0]])

def getE3(alpha, Re, u, dudy):
    return np.array([[-1j*alpha*u - alpha**2/Re, -dudy, -1j*alpha],
                     [0, -1j*alpha*u - alpha**2/Re, 0],
                     [1j*alpha, 0, 0]])

# artificial compressibility added (gamma). See: 
# Khorrami, M. R., Malik, M. R., & Ash, R. L. (1989). Application of spectral collocation techniques
# to the stability of swirling flows. Journal of Computational Physics, 81(1), 206-229.
def getE4():
    gamma = 0.0001
    return np.array([[-1j, 0, 0],
                       [0, -1j, 0],
                       [0, 0, -gamma]])

def get_y(j, h):
    return -1 + h*j

def getA_matrix(alpha, Re, N, comp_num = 3):
    h = 2./N
    matrix_list = list()
    
    # Form first line of matrix A
    line = list()
    y = get_y(1, h)
    u = get_U(y)
    dudy = get_dudy(y)
    E1 = getE1(Re)
    E2 = getE2()
    E3 = getE3(alpha, Re, u, dudy)
    #E4 = getE4()
    L2 = E3 - 2./h**2*E1 #+ 1j*E4
    line.append(L2)
    L3 = 1./h**2*E1 + 1./(2*h)*E2
    line.append(L3)
    for i in range(3,N):
        line.append(np.zeros((comp_num,comp_num)))
    matrix_list.append(line)

    # Form inner lines of matrix A
    for i in range(2, N-1):
        line = list()
        y = get_y(i, h)
        u = get_U(y)
        dudy = get_dudy(y)
        E1 = getE1(Re)
        E2 = getE2()
        E3 = getE3(alpha, Re, u, dudy)
        #E4 = getE4()
        for j in range(1, N):
            if j==i-1:
                L1 = 1./h**2*E1 - 1./(2*h)*E2
                line.append(L1)
            elif j==i:
                L2 = E3 - 2./h**2*E1 #+ 1j*E4
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
    
    y = get_y(N-1, h)
    u = get_U(y)
    dudy = get_dudy(y)
    E1 = getE1(Re)
    E2 = getE2()
    E3 = getE3(alpha, Re, u, dudy)
    #E4 = getE4()
    L1 = 1./h**2*E1 - 1./(2*h)*E2
    line.append(L1)
    L2 = E3 - 2./h**2*E1 # + 1j*E4 
    line.append(L2)
    matrix_list.append(line)

    return np.bmat(matrix_list)

def getB_matrix(alpha, Re, N, comp_num = 3):
    h = 2./N
    #print('h = ', h)
    matrix_list = list()
    for i in range(1,N):
        E4 = getE4()
        matrix_list.append(E4)
    return block_diag(matrix_list).toarray()

class TS_InputParameters(BaseModel):
    Re: float
    alpha: float


    @validator("alpha")
    def check_alpha(cls, alpha):
        if alpha<0.1 or alpha>2 :
            raise ValueError("alpha is out of range! Correct range for alpha = [0.1;2]")
        return alpha
    
    @validator("Re")
    def check_Re(cls, Re):
        if Re<1000 or Re>20000 :
            raise ValueError("Re is out of range! Correct range for Re = [1000, 20000]")
        return Re

def temporal_solve(p: TS_InputParameters) -> np.ndarray:
    N = 400

    alpha = p.alpha
    Re = p.Re
    A = getA_matrix(alpha, Re, N)
    B = getB_matrix(alpha, Re, N)
    # test 1
#    alpha = 1
#    Re = 10000
    eigvals = la.eigvals(A, B)
    eigvals = eigvals/alpha
    return {'data':eigvals}



























