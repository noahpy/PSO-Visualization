#include <stddef.h>
#include <float.h>
#include <math.h>

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

float rast(float* x, size_t n) {
    float result = 10*n;
    for(size_t i=0; i<n; i++) {
        result += x[i]*x[i] - 10 * cosf(M_2_PI*x[i]);
    }
    return result;
}

float schwefel(float* x, size_t n) {
    float result = 0.0f;
    for(size_t i=0; i<n; i++) {
        result += -x[i] * sinf(sqrtf(fabsf(x[i])));
    }
    return result;
}
