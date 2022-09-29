#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include "functions.c"
#include <string.h>

typedef float(*fit_func) (float*, size_t);

fit_func fit_funcs[] = {
    sphere, ros, rast, schwefel, pizza};
const char fit_func_amount = 5;

// gets a two dimensional array of floats with the size n * dim 
// id identifies which fittness function should be used

float call_fittness_func(float* x, size_t n, int func_id){
	if (func_id >= 0 && func_id < fit_func_amount){
		return fit_funcs[func_id](x, n);
	}
	return 0.0f;
}

void run_iter(size_t n, size_t dim, float* particles, float* particle_vels, int func_id, float* best_pos, float* pers_best_list, float vel_w, float soz_w, float cog_w){
	size_t arr_size = n*dim;
	for(size_t i=0; i<arr_size; i++){
		float r1 = ((float)rand()/(float)(RAND_MAX));
		float r2 = ((float)rand()/(float)(RAND_MAX));
		particles[i] = (1-r1*soz_w) * particles[i] + vel_w * particle_vels[i] + (r1*soz_w) * best_pos[i%dim] + cog_w * r2 * (pers_best_list[i]-particles[i]);
	//TODO: update global best and personal best
		if(i%dim == dim-1){
			if(call_fittness_func(&particles[i-(dim-1)],dim,func_id) < call_fittness_func(&pers_best_list[i-(dim-1)],dim,func_id)){
				for(size_t k=0; k<dim; k++){
					pers_best_list[i-(dim-1)+k] = particles[i-(dim-1)+k];
				}
			}
			if(call_fittness_func(&particles[i-(dim-1)],dim,func_id) < call_fittness_func(best_pos,dim, func_id)){
				for(size_t k=0; k<dim; k++){
					best_pos[k] = particles[i-(dim-1)+k];
				}
			}
		}
	}
}







