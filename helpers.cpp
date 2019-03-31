//
// Created by Oleh Rybalchenko on 3/30/19.
//

#include "helpers.h"

double INF = 1000000000;

double ** to2D(double *list, int m, int n) {
    auto D = new double *[m];
    int c = 0;
    for (int i = 0; i < m; i++) {
        D[i] = new double[n];
        for (int j = 0; j < n; j++) {
            D[i][j] = list[c];
            c++;
        }
    }
    return D;
}
