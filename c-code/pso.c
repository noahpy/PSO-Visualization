#include <stddef.h>
#include <stdio.h>
#include "functions.c"

// gets a two dimensional array of floats with the size n * dim 
// id identifies which fittness function should be used

void start_pso(int n, int dim, float particles[n][dim], float particle_vels[n][dim], int id){
	for(int i=0; i<n; i++){
		for(int j=0; j<dim; j++){
			printf("%9.6f\n",particles[i][j]);
		}
	}
}


void update_velocity(){
	
}

void update_position(){

}


void evaluate_fittness(){

}
