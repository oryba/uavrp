//
// Created by Oleh Rybalchenko on 3/31/19.
//

#include "greedy.h"
#include "helpers.h"
#include <vector>
#include <iostream>

double greedy(double *distances, int dim, int n) {
    auto D = HELPERS::to2D(distances, n, n);
    auto visited = new bool[n];
    for (int k = 0; k < n; k++)
        visited[k] = false;
    visited[0] = true;
    auto path = new std::vector<int>;
    int current_id = 0;
    double length = 0;
    path->push_back(current_id);
    for (int iter = 0; iter < n - 1; iter++) {
        int closest_id = -1;
        double closest_dist = HELPERS::INF;
        for (int i = 0; i < n; i++) {
            if (i != current_id && !visited[i] && D[current_id][i] < closest_dist) {
                closest_id = i;
                closest_dist = D[current_id][i];
            }
        }
        if (closest_id == -1) {
            std::cout << "ERROR" << std::endl;
        }
        path->push_back(closest_id);
        visited[closest_id] = true;
        current_id = closest_id;
        length += closest_dist;
    }
    length += D[current_id][0];
    return length;
}