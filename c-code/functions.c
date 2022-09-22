#include <stddef.h>

float sphere(float* x, size_t n) {
    float result = 0.0f;
    for (size_t i; i<n; i++) {
        result += x[i]*x[i];
    }
    return result;
}


