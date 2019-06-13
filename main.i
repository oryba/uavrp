/* main.i */
%module tsp_alg
%{
#define SWIG_FILE_WITH_INIT
extern double bind_data(double * distances, int dim, int n, double p, double a, double b, double ph_min, double ph_max,
                        int iters, int ants);
%}

%include "numpy.i"

%init %{
import_array();
%}

%apply (double* IN_ARRAY1, int DIM1) {(double *distances, int dim)};

extern double bind_data(double * distances, int dim, int n, double p, double a, double b, double ph_min, double ph_max,
                        int iters, int ants);
