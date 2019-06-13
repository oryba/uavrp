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

    best_score = HELPERS::INF;

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


void ACO::update_pheromone(std::vector<int> &path, double score) {
    for (int i = 0; i < data->N; i++) {
        for (int j = 0; j < data->N; j++) {
            // evaporation
            PH[i][j] = max(
                    (1 - data->p) * (PH[i][j] - data->ph_min),
                    data->ph_min
            );
        }
    }

    // update
    if (path.size() == 0)
        return;
    for (int k = 0; k < path.size() - 1; k++) {
        // limit ph from value
        PH[path.at(k)][path.at(k + 1)] = min(
                PH[path.at(k)][path.at(k + 1)] + best_score / score,
                data->ph_max
        );
    }

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
        length += D[path->at(i)][path->at(i + 1)];
    return length;
}

std::vector<int> *ACO::iteration(double &length) {
    // visited vertices
    auto visited = new bool[data->N];
    for (int k = 0; k < data->N; k++)
        visited[k] = false;
    visited[0] = true;

    // current ant's path
    auto path = new std::vector<int>();

    // start from 0 vertex
    int current_id = 0;
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

        auto selected = select_option(*options);

        for (int wp : *selected->path) {
            visited[wp] = true;
            path->push_back(wp);
        }

        current_id = selected->path->back();

        for (Option *obj : *options)
            delete obj;
        options->clear();
        delete options;
    }
    delete visited;
    length = score(path);
    return path;
}


double ACO::run_alg(int I, int J) {
    // basic iteration
    bool non_inc_strategy = false;
    int non_inc_limit = 0;
    if (I < 0) {
        non_inc_strategy = true;
        non_inc_limit = -I;
        I = 10000000;
    }
    int non_inc_steps = 0;
    auto paths = new vector<vector<int>>();
    for (int i = 0; i < I; i++) {
        auto best_on_step = new vector<int>();
        double score_on_step = HELPERS::INF;
        // shared ph runs
        for (int j = 0; j < J; j++) {
            double length = HELPERS::INF;
            auto res = iteration(length);
            paths->push_back(*res);
            if (length < score_on_step) {
                score_on_step = length;
                best_on_step = res;
            }
        }
        if (best_score > score_on_step) {
            non_inc_steps = 0;
            best_score = score_on_step;
            std::cout << "New best " << best_score << " on step #" << i << std::endl;
        }
        else {
            non_inc_steps ++;
            if (non_inc_steps > non_inc_limit) {
                std::cout << "Non-increasing steps limit reached (" << non_inc_steps << ")" <<std::endl;
                break;
            }
        }
        update_pheromone(*best_on_step, score_on_step);

        for (auto obj : *paths) {
            obj.clear();
            obj.resize(0);
        }
        paths->clear();
        paths->resize(0);
    }

    return best_score;
}


Option::Option(double _dist, vector<int> *_path, double _p_num) {
    dist = _dist;
    path = _path;
    p_num = _p_num;
}

Option::~Option() {
    path->clear();
    path->resize(0);
}
