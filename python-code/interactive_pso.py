

#this is a interactive GUI for PSO Visualization and Analysis.

import random as r
from ctypes import *


c_pso = CDLL("../c-code/pso.so")
c_pso.run_iter.argtypes = [c_size_t, c_size_t, POINTER(c_float), POINTER(c_float), c_int]
c_pso.run_iter.restype = None

c_particles = (c_float * 10)()
c_vels = (c_float * 10)()

c_pso.run_iter(5, 2, c_particles, c_vels, 0)

for i in range(10):
    print(c_particles[i])


