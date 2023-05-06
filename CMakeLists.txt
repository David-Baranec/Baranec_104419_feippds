cmake_minimum_required(VERSION 3.25)
project(untitled1)

set(CMAKE_CXX_STANDARD 14)
find_package(MPI REQUIRED)
add_executable(untitled2 main.c)
target_link_libraries(untitled2 PUBLIC MPI::MPI_C)