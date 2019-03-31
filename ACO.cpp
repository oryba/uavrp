//
// Created by Oleh Rybalchenko on 5/11/18.
//

#include "ACO.hpp"
#include "helpers.h"
#include <vector>
#include <iostream>
#include <cmath>
#include <chrono>

using namespace std;


ACO::ACO(Data *_data) {
    data = _data;
    D = data->D;

    // pheromone matrix
    PH = new double *[data->N];
    for (int i = 0; i < data->N; i++) {
        PH[i] = new double[data->N];
        for (int j = 0; j < data->N; j++)
            PH[i][j] = data->ph_min;
    }
}


double ACO::calc_p(double tau, double dist) {
    return pow(tau, data->a) * pow((1 / dist), data->b);
}


double ACO::get_rand() {
    return ((double) rand() / (RAND_MAX));
}


Option *ACO::select_option(std::vector<Option *> &options) {
    double denominator = 0;
    for (auto o : options) {
        denominator += o->p_num;
    }

    auto r = get_rand() * denominator;
    double cum_sum = 0;
    for (auto o : options) {
        if (r < cum_sum + o->p_num)
            return o;
        else
            cum_sum += o->p_num;
    }
    return nullptr;
}

Option *ACO::select_best_option(std::vector<Option *> &options) {
    Option *best = options[0];
    for (auto o : options) {
        if (o->p_num > best->p_num)
            best = o;
    }
    return best;
}

double ACO::score(std::vector<int> *path) {
    double length = D[path->back()][0];
    for (int i = 0; i < path->size() - 1; i++)
        length+=D[path->at(i)][path->at(i+1)];
    return length;
}

double ACO::iteration() {
    // visited vertices
    auto visited = new bool[data->N];
    for (int k = 0; k < data->N; k++)
        visited[k] = false;
    visited[0] = true;

    // current ant's path
    auto path = new std::vector<int>();

    // start from 0 vertex
    int current_id = 0;
    double length = 0;
    path->push_back(current_id);

    for (int iter = 0; iter < data->N - 1; iter++) {
        // all available variants
        auto *options = new vector<Option *>();

        for (int i = 0; i < data->N; i++) {
            if (i != current_id && !visited[i]) {
                // register this way as an option with all its points
                auto way_points = new vector<int>();
                way_points->push_back(i);

                options->push_back(new Option(
                        D[current_id][i], way_points,
                        calc_p(PH[current_id][i], D[current_id][i]) // probability level (numerator)
                ));
            }
        }

        auto selected = select_best_option(*options);

        for (int wp : *selected->path) {
            visited[wp] = true;
            path->push_back(wp);
        }

        current_id = selected->path->back();

        for (Option *obj : *options)
            delete obj;
        options->clear();
    }

    length = score(path);
    return length;
}


double ACO::run_alg(int I) {
    return iteration();
}


Option::Option(double _dist, vector<int> *_path, double _p_num) {
    dist = _dist;
    path = _path;
    p_num = _p_num;
}
