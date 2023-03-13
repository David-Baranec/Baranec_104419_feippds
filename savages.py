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

NUM_SAVAGES: int = 5
NUM_SERVINGS: int = 12


class Shared:
    """Represent shared data for all threads."""
    def __init__(self):
        """Initialize an instance of Shared."""
        self.mutex = Mutex()
        self.servings = NUM_SERVINGS
        self.fullpot = Semaphore(0)
        self.emptypot = Semaphore(0)
        self.barier1 = Semaphore(NUM_SAVAGES)
        self.barier2 = Semaphore(NUM_SAVAGES)


def getservingfrompot(i: int, shared: Shared):
    """Simulate eating.

    Args:
        i -- savage's id
        shared -- shared data
    """
    if shared.servings == 0:
        shared.emptypot.signal()
    else:
        print(f"savage {i} is eating!")
        shared.servings -= 1
    sleep(0.1)


def putservinginpot(shared: Shared):

    while shared.servings < NUM_SERVINGS:
        shared.servings += 1
        print("Meal added to pot")


def savage(i: int, shared: Shared):
    """Run savage's code.

    Args:
        i -- savage's id
        shared -- shared data
    """
    while True:
        shared.barier1.wait("prisli sme na veceru", i)
        shared.mutex.lock()
        if shared.servings == 0:
            shared.emptypot.signal()
            shared.fullpot.wait()
        getservingfrompot(i, shared)
        shared.mutex.unlock()


def cook(shared: Shared):
    while True:
        shared.emptypot.wait()
        putservinginpot(shared)
        shared.fullpot.signal()


def main():
    """Run main."""
    shared: Shared = Shared()
    cook_thread: Thread = Thread(cook, shared)

    savages: list[Thread] = [
        Thread(savage, i, shared) for i in range(NUM_SAVAGES)
    ]
    cook_thread.join()
    for p in savages:
        p.join()


if __name__ == "__main__":
    main()
