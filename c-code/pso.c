#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include "functions.c"

typedef float(*fit_func) (float*, size_t);

fit_func fit_funcs[] = {
    sphere, ros, rast, schwefel, pizza};
const char fit_func_amount = 5;

// gets a two dimensional array of floats with the size n * dim 
// id identifies which fittness function should be used

void run_iter(size_t n, size_t dim, float* particles, float* particle_vels, int func_id, float* best_pos){
	for(size_t i=0; i<n*dim; i++){
		printf("%9.6f\n",particles[i]);
	}
}


void update_velocity(){
	
}

void update_position(){

}


void evaluate_fittness(){

}
