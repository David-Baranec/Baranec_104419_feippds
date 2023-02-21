"""This module contains an implementation of bakery algorithm.

Bakery Algorithm is an algorithm that basically works as a generalized solution for the critical section problem,
 that means for N processes.
"""

__author__ = "David Baranec, Tomáš Vavro"
__email__ = "xbaranecd@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread
from time import sleep

tickets: tickets = [0, 1, 2, 3, 4]
entering: entering = [False] * 5


def process(tid: int, num_runs: int):
    """Simulates a process.

    Arguments:
        tid      -- thread id
        num_runs -- number of executions of the critical section
    """
    global tickets, entering

    for _ in range(num_runs):

        # process wants to enter critical section
        entering[tid] = True

        maximum = 0
        for ticket in tickets:
            maximum = max(maximum, ticket)
        tickets[tid] = maximum + 1
        entering[tid] = False
        for i in range(len(tickets)):

                # Wait until thread j receives its number:
            while entering[i]:
                 print("waiting on enter")

                # Wait until all threads with smaller numbers or with the samenumber, but with higher priority, finish their work:
            while tickets[i] != 0 and (tickets[tid] > tickets[i] or (tickets[tid] == tickets[i] and tid > i)):
                 print("waiting")

            ###########################
        # execute critical section
        print(f"Process {tid} runs a complicated computation!")
        #sleep(1)

        # exit critical section
        tickets[tid] = 0

if __name__ == '__main__':
    DEFAULT_NUM_RUNS = 5
    NUM_THREADS = 3
    threads = [Thread(process, i, DEFAULT_NUM_RUNS) for i in range(NUM_THREADS)]
    [t.join() for t in threads]