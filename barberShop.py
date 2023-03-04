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

        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def get_haircut(i):
    print(f"Customer: {i} gets haircut")
    sleep(randint(3,5))

def cut_hair():
    print("Barber: cuts hair!")
    sleep(randint(3,5))


def balk(i):
    print(f"Customer: {i} waiting room is full!")
    sleep(randint(5,8))


def growing_hair(i):

    sleep(randint(8,14))


def customer(i, shared):
    global N

    while True:
        shared.mutex.lock()
        if (shared.waiting_room<N ):
            print(f"Customer: {i} is in the room!")
            shared.waiting_room+=1
            shared.mutex.unlock()

            shared.customer.signal()
            shared.barber.wait()

            get_haircut(i)
            print(f"Customer: {i} left!")

            shared.barber_done.signal()
            shared.customer_done.wait()

            shared.mutex.lock()
            shared.waiting_room -= 1
            shared.mutex.unlock()
            growing_hair(i)

        else:
            shared.mutex.unlock()
            balk(i)




def barber(shared):

    while True:
        shared.customer.wait()
        shared.barber.signal()

        cut_hair()

        shared.barber_done.wait()
        shared.customer_done.signal()


def main():
    global C, N
    shared = Shared()
    customers = []

    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()



if __name__ == "__main__":
    main()