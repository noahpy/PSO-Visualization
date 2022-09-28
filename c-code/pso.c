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

void run_iter(size_t n, size_t dim, float* particles, float* particle_vels, int func_id, float* best_pos, float* pers_best_list, float vel_w, float soz_w, float cog_w){
	size_t arr_size = n*dim;
	float* pers_best_cpy = malloc(arr_size*4);
	if (pers_best_cpy == NULL){
		return;
	}
	memcpy(pers_best_cpy, pers_best_list, arr_size*4);
	for(size_t i=0; i<arr_size; i++){
		
	}
}


void update_velocity(){
	
}

void update_position(){

}


void evaluate_fittness(){

}



