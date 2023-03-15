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
        self.servings = NUM_SERVINGS
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
    print(f"savage {i} takes meal!")
    shared.servings -= 1
    print(f"savage {i} is eating!")
    sleep(0.2)


def putservinginpot(i: int, shared: Shared):
        shared.servings += 1
        sleep(0.2)
        print(f"Meal {shared.servings} was added to pot by chef {i} !")

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
            print("\nAll of us are here\n")
            shared.barier1.signal(NUM_SAVAGES)

        shared.barier1.wait()
        shared.mutex.lock()
        if shared.servings > 0:
            getservingfrompot(i, shared)
            shared.mutex.unlock()

        else:
            shared.mutex.unlock()
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
        shared.mutex.lock()
        if shared.servings == 0:
            print(" Pot is empty Starts cooking")
        shared.mutex.unlock()

        while shared.servings < NUM_SERVINGS:
            shared.mutex.lock()
            if shared.servings < NUM_SERVINGS:
                putservinginpot(i, shared)
                sleep(0.1)
            shared.mutex.unlock()

        shared.fullpot.signal()




def main():
    """Run main."""
    shared: Shared = Shared()
    cooks: list[Thread] = [
        Thread(cook, i, shared) for i in range(NUM_COOKS)
    ]
    savages: list[Thread] = [
        Thread(savage, i, shared) for i in range(NUM_SAVAGES)
    ]
    for p in cooks:
        p.join()
    for p in savages:
        p.join()


if __name__ == "__main__":
    main()
