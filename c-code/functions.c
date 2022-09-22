#include <stddef.h>

float sphere(float* x, size_t n) {
    float result = 0.0f;
    for(size_t i=0; i<n; i++) {
        result += x[i]*x[i];
    }
    return result;
}

float ros(float* x, size_t n) {
    float result = 0.0f;
    float exp1;
    for(size_t i=0; i<n-1; i++) {
        exp1 = x[i+1] - x[i]*x[i];
        result += 100 * (exp1*exp1) + (1-x[i])*(1-x[i]);
    }
    return result;
}

