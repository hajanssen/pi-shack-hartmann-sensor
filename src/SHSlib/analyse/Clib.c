
// compilation Command:
// gcc -Wall -pedantic -shared -fPIC -O3 -o mylib.so main.c

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void sumPerLable(unsigned int *img, size_t n_img,
                 unsigned int *lable, size_t n_lable, 
                 unsigned int *M00, size_t n_M00){

    for (size_t i = 0; i < n_img; i++){
        M00[lable[i]] = img[i] + M00[lable[i]];
    }
    return;
}


void getMomentum(unsigned long *img, size_t n_img,
                   unsigned long *lable, size_t n_lable,
                   unsigned long *X, size_t n_X,
                   unsigned long *Y, size_t n_Y,
                   double *X_Pos, size_t n_X_Pos,
                   double *Y_Pos, size_t n_Y_Pos)
    {
    
    // allocation of arrays for
    unsigned long *M00 = calloc(n_X_Pos, sizeof(unsigned long));
    unsigned long *M01 = calloc(n_X_Pos, sizeof(unsigned long));
    unsigned long *M10 = calloc(n_X_Pos, sizeof(unsigned long));

    // sum up values to get momentum elementes
    for (size_t i = 0; i < n_img; i++){
        M00[lable[i]] = img[i] + M00[lable[i]];
        M10[lable[i]] = (img[i] * X[i]) + M10[lable[i]];
        M01[lable[i]] = (img[i] * Y[i]) + M01[lable[i]];
    }
    
    // calculate centroid from momenta
    for (size_t i = 0; i < n_X_Pos; i++){
        X_Pos[i] = (double) M01 [i] / M00[i];
        Y_Pos[i] = (double) M10[i] / M00[i];
    }
    
    // free allocated memeory
    free(M00);
    free(M01);
    free(M10);
    
    return;
}

int main()
{
}


































