"""This module implement image conversion to grayscale in cuda using numba, comparing CPU and GPU performance.
"""

__authors__ = "Dávid Baranec"
__licence__ = "MIT"

import numpy as np
from PIL import Image
from numba import cuda
import time


@cuda.jit
def grayscale_kernel(image_gpu):
    """Convert data representing colorful picture to grayscale data.

    Arguments:
    image_gpu -- data describing image  for processing
    """
    x, y = cuda.grid(2)
    if x < image_gpu.shape[0] and y < image_gpu.shape[1]:
        r, g, b = image_gpu[x, y]
        gray_value = 0.299 * r + 0.587 * g + 0.114 * b
        image_gpu[x, y] = [gray_value, gray_value, gray_value]


def main():
    """ Main program loading data and processing  cpu and gpu transformation to grayscale comparing time of operations."""
    name = "city"
    image = Image.open('images/'+name+'.jpg')
    # Convert the image to a NumPy array
    image_np = np.array(image)
    # Convert the image to grayscale using CPU
    start_time_cpu = time.time()
    image_gray_cpu = np.dot(image_np[..., :3], [0.299, 0.587, 0.114])
    end_time_cpu = time.time()

    # Check if CUDA is available
    if not cuda.is_available():
        print("CUDA is not available. Please make sure you have an NVIDIA GPU.")
        exit()
    cuda.select_device(0)
    # Transfer the image to the GPU
    image_gpu = cuda.to_device(image_np)
    # Set the block size and grid size for the GPU
    block_size = (16, 16)
    grid_size = ((image_np.shape[0] + block_size[0] - 1) // block_size[0],
                 (image_np.shape[1] + block_size[1] - 1) // block_size[1])

    # Launch the kernel function on the GPU
    start_time_gpu = time.time()

    grayscale_kernel[grid_size, block_size](image_gpu)
    cuda.synchronize()

    end_time_gpu = time.time()

    # Transfer the grayscale image back to the CPU
    image_gray_gpu = image_gpu.copy_to_host()

    # Create a PIL image from the grayscale array
    image_gray_pil = Image.fromarray(image_gray_gpu.astype(np.uint8))

    # Save the grayscale image
    # Create a PIL image from the grayscale array
    image_gray_pil.save('images/output_'+name+'.jpg')

    # Print the execution times
    print("CPU execution time:", end_time_cpu - start_time_cpu, "seconds")
    print("GPU execution time:", end_time_gpu - start_time_gpu, "seconds")


if __name__ == "__main__":
    main()
