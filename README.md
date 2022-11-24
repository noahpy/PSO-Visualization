# Particle Swarm Optimization Visualization

## Motivation:
This program was created for the **Ferienakademie** course
**Modern Approaches to Optimization and Verification**, where I 
worked on Particle Swarm optimization. The aim of this program was 
to visualize the Particle Swarm Optimization nicely, while still maintaining
very good performance and proving the power of this method.

## How I built it:
Because of the stated motivation above, I decided to split up 
the visualization to be implemented in Python and the PSO at its
core in C. 

### The PSO-Module
The PSO-Module, written in C, takes the most computational work of
the method. It takes references to the arrays of positions, velocities
and past best positions of the particles and the global best position.
With this information, it will operate on the array and update its values.
The C program will be compiled into a share library (look at the Makefile!),
so that the visualization program can call it with the help of ctypes.

### The Visualization-Program
I used Panda3D, a render engine for 
rendering PSO, as it promised to be fast and effective as it is written 
in C++. It first takes initial inputs like the amount of particles
and their restriction and then generates those initial positions 
and velocities, etc. Then it will pass those references to the PSO-Module
and the values get updated. The results are visualized in a 3D-visualization.

## Next Steps:
* Use vectorization / intrinsics in PSO-Module to gain even more speed!
* Fix some visualization issues
* Implement Discrete Particle Optimization and its visualization

## Results:
Those are some results of the current program.

<img src=/assets/images/schwefel.jpg>
<sub>Particle Swarm Optimization on Schwefel Function</sub>


<img src=/assets/images/pizzs.jpg>
<sub>Particle Swarm Optimization on Pizza Function</sub>






