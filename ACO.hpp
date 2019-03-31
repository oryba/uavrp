//
// Created by Oleh Rybalchenko on 5/11/18.
//

#include <vector>
#include "data.hpp"

#ifndef DIPLOMA_ACO_H
#define DIPLOMA_ACO_H


class Option {
public:
    Option(double _dist, std::vector<int> *_path, double _p_num);

    double dist, p_num; // additional distance, probability numerator
    std::vector<int> *path;
};


class ACO {
public:
    ACO(Data *data);

    double ** D;

    double run_alg(int I);

    // void reset();
    constexpr static double INF = 999999990;


private:
    Data *data;
    double **PH;
    double iteration();

    // calculate a probability for given ph and distance
    double calc_p(double tau, double dist);

    // select weighted random option
    Option *select_option(std::vector<Option *> &options);

    // select best option, no random
    Option *select_best_option(std::vector<Option *> &options);

    double get_rand();

    double score(std::vector<int> *path);

};


#endif //DIPLOMA_ACO_H