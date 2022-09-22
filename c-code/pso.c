#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include "functions.c"

// gets a two dimensional array of floats with the size n * dim 
// id identifies which fittness function should be used

void start_pso(int n, int dim, float** particles, float** particle_vels, int id){
	float (*fittness_function)(float*, size_t);
	float lowerbound, higherbound;
	switch(id){
		case 0:
			fittness_function = *sphere;
			break;
		default:
			return;
		}


	void* tmp = malloc(n*dim*sizeof(float));
	if(tmp == NULL){
		exit(69);
	}
	float* p = (float*) tmp;
	for(int i=0; i<n*dim; i++){
		p[i] = 3.1415926;
	}
	*particles = p;
}

void stop_pso(float* particles, float* vels){
	free(particles);
	free(vels);
}


void update_velocity(){
	
}

void update_position(){

}


void evaluate_fittness(){

}
