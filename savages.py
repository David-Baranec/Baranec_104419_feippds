"""This module implements dinning savages problem.

 #####################
 """

__author__ = "Dávid Baranec"
__email__ = "xbaranecd@stuba.sk"
__license__ = "MIT"
__web_sources__ = "################"

from fei.ppds import Thread, Mutex, Semaphore
from time import sleep
from fei.ppds import print

NUM_COOKS: int = 2
NUM_SAVAGES: int = 5
NUM_SERVINGS: int = 12


class Shared:
    """Represent shared data for all threads."""
    def __init__(self):
        """Initialize an instance of Shared."""
        self.mutex = Mutex()
        self.servings = 0
        self.fullpot = Semaphore(0)
        self.emptypot = Semaphore(0)
        self.barier1 = Semaphore(0)
        self.barier2 = Semaphore(0)
        self.count = 0


def getservingfrompot(i: int, shared: Shared):
    """Simulate eating.

    Args:
        i -- savage's id
        shared -- shared data
    """
    shared.mutex.lock()
    shared.servings -= 1
    shared.mutex.unlock()
    print(f"savage {i} is eating!")
    sleep(0.1)


def putservinginpot(i: int, shared: Shared):
    while shared.servings < NUM_SERVINGS:
        shared.mutex.lock()
        shared.servings += 1
        shared.mutex.unlock()
        print(f"Meal {shared.servings} was added to pot by {i} cook!")
        sleep(0.1)


def savage(i: int, shared: Shared):
    """Run savage's code.

    Args:
        i -- savage's id
        shared -- shared data
    """
    while True:
        shared.mutex.lock()
        shared.count += 1
        shared.mutex.unlock()

        if shared.count == NUM_SAVAGES:
            print("All of us are here")
            shared.barier1.signal(NUM_SAVAGES)

        shared.barier1.wait()
        if shared.servings > 0:
            getservingfrompot(i, shared)
        else:
            shared.emptypot.signal()
            shared.fullpot.wait()
        shared.mutex.lock()
        shared.count -= 1
        shared.mutex.unlock()

        if shared.count == 0:
            shared.barier2.signal(NUM_SAVAGES)
        shared.barier2.wait()


def cook(i: int, shared: Shared):
    while True:
        shared.emptypot.wait()
        putservinginpot(i, shared)
        shared.fullpot.signal()


def main():
    """Run main."""
    shared: Shared = Shared()
    #cook_thread: Thread = Thread(cook, shared)
    cooks: list[Thread] = [
        Thread(cook, i, shared) for i in range(NUM_COOKS)
    ]
    savages: list[Thread] = [
        Thread(savage, i, shared) for i in range(NUM_SAVAGES)
    ]
    #cook_thread.join()
    for p in cooks:
        p.join()
    for p in savages:
        p.join()


if __name__ == "__main__":
    main()
