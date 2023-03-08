"""This module implements dinning philosophers problem.

 No solution is implemented.
 """

__author__ = "Dávid Baranec"
__email__ = "xbaranecd@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"
__web_sources__ = "https://zerobone.net/blog/cs/dining-philosophers-problem/?fbclid" \
                  "=IwAR0EqklHeVGqOeV_mwcvFqWx4R0aBGbA6sf92CgjX1NWmDbPoCBPN6rva5U "

from fei.ppds import Thread, Mutex
from time import sleep
from fei.ppds import print

NUM_PHILOSOPHERS: int = 5
NUM_RUNS: int = 10  # number of repetitions of think-eat cycle of philosophers


class Shared:
    """Represent shared data for all threads."""
    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]


def think(i: int):
    """Simulate thinking.

    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is thinking!")
    sleep(0.1)


def eat(i: int):
    """Simulate eating.

    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is eating!")
    sleep(0.1)


def philosopher(i: int, shared: Shared):
    """Run philosopher's code.

    Args:
        i -- philosopher's id
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        # Philosopher number 1 prefers left fork, and then he grabs the right one
        if i == 1:
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
            print(f" {(i + 1) % NUM_PHILOSOPHERS} fork is taken by {i}")
            shared.forks[i].lock()
            print(f" {i} fork is taken by {i}")
            eat(i)
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
            print(f" {(i + 1) % NUM_PHILOSOPHERS} fork is left by {i}")
            shared.forks[i].unlock()
            print(f" {i} fork is left by {i}")
        else:
            shared.forks[i].lock()
            print(f" {i} fork is taken by {i}")
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
            print(f" {(i + 1) % NUM_PHILOSOPHERS} fork is taken by {i}")
            eat(i)
            shared.forks[i].unlock()
            print(f" {i} fork is left by {i}")
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
            print(f" {(i + 1) % NUM_PHILOSOPHERS} fork is left by {i}")


def main():
    """Run main."""
    shared: Shared = Shared()
    philosophers: list[Thread] = [
        Thread(philosopher, i, shared) for i in range(NUM_PHILOSOPHERS)
    ]
    for p in philosophers:
        p.join()


if __name__ == "__main__":
    main()
