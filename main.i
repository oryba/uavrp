/* main.i */
%module tsp_alg
%{
#define SWIG_FILE_WITH_INIT
extern double bind(double * distances, int dim, int n);
%}

%include "numpy.i"

%init %{
import_array();
%}

%apply (double* IN_ARRAY1, int DIM1) {(double *distances, int dim)};

extern double bind(double * distances, int dim, int n);
