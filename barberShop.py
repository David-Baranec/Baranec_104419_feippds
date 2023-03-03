"""
Program represents different sequences of using mutex

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""


__authors__ = "Dávid Baranec, Marián Šebeňa"
__email__ = "xbaranecd@stuba.sk, mariansebena@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"


from fei.ppds import Mutex, Thread, Semaphore
from time import sleep
from random import randint
from fei.ppds import print

C: C = 5
N: N = 3
"""
Global arguments:
    C      -- Number of customers
    N      -- Size of waiting room
"""
class Shared(object):

    def __init__(self):

        # TODO : Initialize patterns we need and variables
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = 0
        self.barber_done = 1


def get_haircut(i):
    # TODO: Simulate time and print info when customer gets haircut
    print(f"Customer: {i} cuts hair")
    sleep(2)


def cut_hair():
    # TODO: Simulate time and print info when barber cuts customer's hair
    print("cuts hair!")
    sleep(3)


def balk(i):
    # TODO: Represents situation when waiting room is full and print info
    print(f"Customer: {i} waiting room is full!")
    sleep(2)


def growing_hair(i):
    # TODO: Represents situation when customer wait after getting haircut. So hair is growing and customer is sleeping for some time
    print(f"Customer: {i} hair is growing!")
    sleep(10)


def customer(i, shared):
    # TODO: Function represents customers behaviour. Customer come to waiting if room is full sleep.
    # TODO: Wake up barber and waits for invitation from barber. Then gets new haircut.
    # TODO: After it both wait to complete their work. At the end waits to hair grow again
    global N
    shared.mutex.lock()
    while True:
        # TODO: Access to waiting room. Could customer enter or must wait? Be careful about counter integrity :)
        if (shared.waiting_room<N):
            print(f"Customer: {i} is in the room!")

            shared.waiting_room+=1
            shared.customer.signal()
            shared.mutex.unlock()
            shared.barber.wait()
            shared.barber_done=0
        # TODO: Rendezvous 1
            get_haircut(i)
        # TODO: Rendezvous 2
        else:
            shared.mutex.unlock()
            balk(i)
        # TODO: Leave waiting room. Integrity again
        growing_hair(i)


def barber(shared):
    # TODO: Function barber represents barber. Barber is sleeping.
    # TODO: When customer come to get new hair wakes up barber.
    # TODO: Barber cuts customer hair and both wait to complete their work.

    while True:
        if (shared.waiting_room==0 and shared.barber_done==1):
            print("Nobody is here. I'm going to sleep");
        shared.customer.wait()
        shared.mutex.lock()
        if (shared.waiting_room>0):
            shared.waiting_room-=1
        shared.barber.signal()
        shared.mutex.unlock()


        # TODO: Rendezvous 1
        cut_hair()
        # TODO: Rendezvous 2


def main():
    global C, N
    shared = Shared()
    customers = []

    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()

# TODO: Global variables C = 5 numOfCustomers N = 3 sizeOfWaitingRoom


if __name__ == "__main__":
    main()