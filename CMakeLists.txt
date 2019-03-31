cmake_minimum_required(VERSION 3.10)
project(tsp)

set(CMAKE_CXX_COMPILER /usr/local/opt/llvm/bin/clang++)

set(CMAKE_CXX_STANDARD 11)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -fopenmp")

add_executable(tsp main.cpp main.i helpers.h helpers.cpp greedy.h greedy.cpp
        data.cpp
        data.hpp
        ACO.cpp ACO.hpp)