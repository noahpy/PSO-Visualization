#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include <float.h>
#include <math.h>

float sphere(float* x, size_t n) {
    float result = 0.0f;
    for(size_t i=0; i<n; i++) {
        if (x[i] < -100 || x[i] > 100)
            return INFINITY;

        result += x[i]*x[i];
    }
    return result;
}

float ros(float* x, size_t n) {
    float result = 0.0f;
    float exp1;
    for(size_t i=0; i<n-1; i++) {
        if (x[i] < -30 || x[i] > 30)
            return INFINITY;

        exp1 = x[i+1] - x[i]*x[i];
        result += 100 * (exp1*exp1) + (1-x[i])*(1-x[i]);
    }
    return result;
}

float rast(float* x, size_t n) {
    float result = 10*n;
    for(size_t i=0; i<n; i++) {
        if (x[i] < -5.12f || x[i] > 5.12f)
            return INFINITY;

        result += x[i]*x[i] - 10 * cosf(M_2_PI*x[i]);
    }
    return result;
}

float schwefel(float* x, size_t n) {
    float result = 0.0f;
    for(size_t i=0; i<n; i++) {
        if (x[i] < -500 || x[i] > 500)
            return INFINITY;

        result += -x[i] * sinf(sqrtf(fabsf(x[i])));
    }
    return result;
}

// compare function for floats used for qsort
int compf(const void* a, const void* b) {
    float x = *(float*) a;
    float y = *(float*) b;
    if (x < y)
        return -1;
    if (x > y)
        return 1;
    return 0;
}

float pizza(float* x, size_t n) {
    float result = sphere(x, n);
    qsort(x, n, sizeof(float), compf);

    if (x[0] < -100 || x[n-1] > 100)
        return INFINITY;

    if (x[0] * 1.1f > x[n-1]) {
        float max = 0.0f;
        if (x[n-1] > 0 && x[0] > 0) {
            max = x[n-1] / x[0];
        } else if (x[n-1] < 0 && x[0] < 0) {
            max = x[0] / x[n-1];
        } else {
            size_t i = 0;
            while (x[i] <= 0)
                i++;
            if (i != n-1) {
                max = x[n-1] / x[i];
            }
            while (x[i] >= 0)
                i--;

            if (i != 0) {
                max = max >= x[0] / x[i] ? max : x[0] / x[i];
            }
        }
        result *= 10 * (2 * max - 2.1);
    }
    return result;
}

