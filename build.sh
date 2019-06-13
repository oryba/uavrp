#!/usr/bin/env bash
cd manager/bind
swig -python -c++ -o aco_wrap.cpp ../../main.i
g++ -c -std=c++11 -arch x86_64 -fPIC ../../*.cpp \
    -I ..
g++ -c -std=c++11 -arch x86_64 -fPIC aco_wrap.cpp -o aco_wrap.o \
    -I/Library/Frameworks/Python.framework/Versions/3.7/include/python3.7m \
    -I/Users/oryba/envs/venv/lib/python3.7/site-packages/numpy/core/include
ld -bundle -macosx_version_min 10.13 -flat_namespace -undefined suppress -o _tsp_alg.so *.o
