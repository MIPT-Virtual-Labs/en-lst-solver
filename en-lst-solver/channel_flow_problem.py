# Plane poiseuille flow profile
def get_U(y):
    return 1 - y**2

def get_dudy(y):
    return -2*y