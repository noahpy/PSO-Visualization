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

void start_pso(int n, int dim, float** particles, float** particle_vels, int func_id){
    if (func_id < 0 || func_id >= fit_func_amount) {
        fprintf(stderr, "Error: invalid func_id");
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
