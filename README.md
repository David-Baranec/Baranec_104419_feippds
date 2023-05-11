# Baranec_104419_feippds
Repozitár k zadaniam z predmetu PPDS pre letný semester 2023, Fakulta Elektrotechniky a Informatiky Slovenskej Technickej Univerzity v Bratislave

Assignment 05: Convert colorful image to grayscale using CPU and GPU

# Introduction
The main purpose of this program is to demonstrate effectivity of CUDA. 
CUDA (or Compute Unified Device Architecture) is a parallel computing platform and application programming interface.
CUDA is designed to work with programming languages such as C, C++, and Fortran. This accessibility makes it easier for specialists in parallel programming to use GPU resources.
With GPU you can perform thousands of calculates many times faster than on CPU.

# Solution
Program demonstrates using numba library to perform CUDA computation in python. Firstly it is defined `CUDA JIT` is a low-level entry point to the CUDA features in Numba.
Data are processed as values in arrays. The code assigns the red (r), green (g), and blue (b) components of the pixel at coordinates (x, y) to the variables r, g, and b, respectively. 
The code calculates the grayscale value by multiplying each color component (r, g, b) by a specific weight and summing them up.
The weights used here are the standard luminance coefficients often used in image processing: 0.299 for red, 0.587 for green, and 0.114 for blue. 
These values represent the human perception of brightness for each color channel.

# Results
The main perform computation for CPU in serial mode and also GPU computation using NUMBA. Both are stored in separate files with appropriate name. 
In table are results for time performance in seconds based on frame resolution.
![comparison_table.png](img.png)

Comparison table does not show as good results as we have expected in theoretical model. But this is caused by emulator for GPU, which does not give enough performance as full computing performance of GPU.
However, these results are not fixed times, they represent average time  of computing. 
# TO RUN
Install package `numba`. After installation add `NUMBA_ENABLE_CUDASIM=1` to environment variables and run `main.py`.  