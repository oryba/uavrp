//
//  data.hpp
//  diploma
//
//  Created by Oleh Rybalchenko on 5/11/18.
//  Copyright © 2018 Oleh Rybalchenko. All rights reserved.
//

#ifndef data_hpp
#define data_hpp

#include <stdio.h>

class Data {
public:
    Data(int N, double **D, double p, double a, double b, double ph_min, double ph_max): N(N), D(D), p(p), a(a), b(b), ph_min(ph_min),
    ph_max(ph_max) {};

    double **D;
    int N;
    double p, a, b, ph_min, ph_max;
    bool two_steps = false;

private:

};


#endif /* data_hpp */
