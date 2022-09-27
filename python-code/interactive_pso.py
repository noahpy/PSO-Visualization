

#this is a interactive GUI for PSO Visualization and Analysis.

import random as r
from ctypes import *
from direct.showbase.ShowBase import ShowBase

particle_amount = 5
dimensions = 2

c_pso = CDLL("../c-code/pso.so")
c_pso.run_iter.argtypes = [c_size_t, c_size_t, POINTER(c_float), POINTER(c_float), c_int, POINTER(c_float)]
c_pso.run_iter.restype = None

c_particles = (c_float * (particle_amount*dimensions))()
c_vels = (c_float * (particle_amount*dimensions))()
c_best_pos = (c_float * dimensions)()

c_pso.run_iter(particle_amount, dimensions, c_particles, c_vels, 0, c_best_pos)

for i in range(particle_amount*dimensions):
    print(c_particles[i])


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)


app = MyApp()
app.run()


