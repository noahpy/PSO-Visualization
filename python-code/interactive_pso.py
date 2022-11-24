

#this is a interactive GUI for PSO Visualization and Analysis.
from pso_render import PSO_App
import random as r
from ctypes import *
import threading as th
import queue as q


particle_amount = 50
dimensions = 2
vel_w = 0.5
cog_w = 1.
soz_w = 1.
func_id = 4
bounds_dict = [(-100,100),(-30,30),(-5.12,5.12),(-500,500),(-100,100)]

c_pso = CDLL("../c-code/pso.so")
c_pso.run_iter.argtypes = [c_size_t, c_size_t, POINTER(c_float), POINTER(c_float), c_int, POINTER(c_float), POINTER(c_float), c_float, c_float, c_float]
c_pso.run_iter.restype = None
c_pso.call_fittness_func.argtypes = [POINTER(c_float), c_size_t, c_int]
c_pso.call_fittness_func.restype = c_float


def blackbox_func(x,y):
    global func_id
    c_coordinates = (c_float * dimensions)()
    c_coordinates[0] = x
    c_coordinates[1] = y
    result = c_pso.call_fittness_func(c_coordinates, 2, func_id)
    return result


particles = []
vels = []
best_pos = []
for i in range(particle_amount * dimensions):
    particles.append(r.uniform(bounds_dict[func_id][0], bounds_dict[func_id][1]))
    vels.append(r.uniform(bounds_dict[func_id][0], bounds_dict[func_id][1]) * 0.2)
    if i%2 == 1:
        if len(best_pos) != 2 or blackbox_func(particles[i-1],particles[i]) < blackbox_func(best_pos[0], best_pos[1]):
            best_pos = [particles[i-1],particles[i]]
    

c_particles = (c_float * (particle_amount*dimensions))(*particles)
c_vels = (c_float * (particle_amount*dimensions))(*vels)
c_pers_bests = (c_float * (particle_amount*dimensions))(*particles)
c_best_pos = (c_float * dimensions)(*best_pos)



result_queue = q.Queue()

def run_pso():
    global result_queue
    convergence_count = 0
    p_best = [0,0]
    while convergence_count < 100:
        c_pso.run_iter(particle_amount, dimensions, c_particles, c_vels, func_id, c_best_pos, c_pers_bests, vel_w, soz_w, cog_w)
        copy = []
        for n in c_particles:
            copy.append(n)
        result_queue.put(copy)
        r = "best position: "
        for n in c_best_pos:
            r += str(n)+ ", "
        print(r)
        convergence_flag = p_best != []
        for i in range(len(p_best)):
            convergence_flag &= round(p_best[i], 5) == round(c_best_pos[i], 5)
        if convergence_flag:
            convergence_count+=1
        else:
            convergence_count = 0
        for i in range(len(p_best)):
            p_best[i] = c_best_pos[i]

pso = th.Thread(target=run_pso)
pso.start()

app = PSO_App(result_queue, func_id, c_particles, fittness_function=blackbox_func, xbound=bounds_dict[func_id], ybound=bounds_dict[func_id])
app.run()








