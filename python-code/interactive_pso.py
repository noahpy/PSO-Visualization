

#this is a interactive GUI for PSO Visualization and Analysis.

import random as r
from ctypes import *


c_pso = CDLL("../c-code/pso.so")
c_pso.start_pso.argtypes = [c_int, c_int, POINTER(POINTER(c_float)), POINTER(POINTER(c_float)), c_int]
c_pso.start_pso.restype = None
c_pso.stop_pso.argtypes = [POINTER(c_float), POINTER(c_float)]
c_pso.stop_pso.restype = None

c_particles = POINTER(c_float)()
c_vels = POINTER(c_float)()

c_pso.start_pso(5, 2, c_particles, c_vels, 0)

for i in range(10):
    print(c_particles[i])

c_pso.stop_pso(c_particles, c_vels)

