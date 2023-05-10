import numba
from numba import cuda


def main():
    print(cuda.is_available())
    print(cuda.gpus)
    numba.cuda.select_device(0)


if __name__ == "__main__":
    main()
