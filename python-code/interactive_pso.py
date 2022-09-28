

#this is a interactive GUI for PSO Visualization and Analysis.
from pso_render import PSO_App
import random as r
from ctypes import *


particle_amount = 5
dimensions = 2
vel_w = 0.5
cog_w = 1
soz_w = 1

c_pso = CDLL("./c-code/pso.so")
c_pso.run_iter.argtypes = [c_size_t, c_size_t, POINTER(c_float), POINTER(c_float), c_int, POINTER(c_float), c_float, c_float, c_float]
c_pso.run_iter.restype = None

c_particles = (c_float * (particle_amount*dimensions))()
c_vels = (c_float * (particle_amount*dimensions))()
c_pers_bests = (c_float * (particle_amount*dimensions))()
c_best_pos = (c_float * dimensions)()


c_pso.run_iter(particle_amount, dimensions, c_particles, c_vels, 0, c_best_pos, c_pers_bests, vel_w, soz_w, cog_w)

for i in range(particle_amount*dimensions):
    #print(c_particles[i])
    pass

app = PSO_App()
app.run()




