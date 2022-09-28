

#this is a interactive GUI for PSO Visualization and Analysis.
from pso_render import PSO_App
import random as r
from ctypes import *


particle_amount = 5
dimensions = 2
vel_w = 0.5
cog_w = 1.
soz_w = 1.
func_id = 0
bounds_dict = [(-100,100),(-30,30),(-5.12,5.12),(-500,500),(-100,100)]

c_pso = CDLL("./c-code/pso.so")
c_pso.run_iter.argtypes = [c_size_t, c_size_t, POINTER(c_float), POINTER(c_float), c_int, POINTER(c_float), POINTER(c_float), c_float, c_float, c_float]
c_pso.run_iter.restype = None
c_pso.call_fittness_func.argtypes = [POINTER(c_float), c_size_t, c_int]
c_pso.call_fittness_func.restype = c_int


particles = []
for i in range(particle_amount * dimensions):
    particles.append(r.uniform(bounds_dict[func_id][0], bounds_dict[func_id][1]))

c_particles = (c_float * (particle_amount*dimensions))(*particles)
c_vels = (c_float * (particle_amount*dimensions))()
c_pers_bests = (c_float * (particle_amount*dimensions))()
c_best_pos = (c_float * dimensions)()


def blackbox_func(x,y):
    global func_id
    c_coordinates = (c_float * dimensions)()
    c_coordinates[0] = x
    c_coordinates[1] = y
    result = c_pso.call_fittness_func(c_coordinates, 2, func_id)
    return result
    


c_pso.run_iter(particle_amount, dimensions, c_particles, c_vels, 0, c_best_pos, c_pers_bests, vel_w, soz_w, cog_w)

app = PSO_App(c_particles, fittness_function=blackbox_func)
app.run()




