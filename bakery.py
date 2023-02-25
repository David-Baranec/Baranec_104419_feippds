"""This module contains an implementation of bakery algorithm.

Bakery Algorithm is an algorithm that basically works as a generalized solution for the critical section problem,
 that means for N processes.
"""

__authors__ = "David Baranec, Tomáš Vavro, Yash Boura"
__email__ = "xbaranecd@stuba.sk"
__license__ = "MIT"
__web_sources__ = "https://cppsecrets.com/users/120612197115104981111171149751485164103109971051084699111109/Python-Implementation-of-Bakery-Algorithm.php"

from fei.ppds import Thread
from time import sleep

tickets: tickets = [0,1,2,3,4,5]
entering: entering = [0] * 6

def process(tid: int, num_runs: int):
    """Simulates a process.

    Arguments:
        tid      -- thread id
        num_runs -- number of executions of the critical section
    """
    global tickets, entering

    for _ in range(num_runs):

        # process wants to enter critical section
        entering[tid] = 1

        maximum = 0
        for ticket in tickets:
            maximum = max(maximum, ticket)
        tickets[tid] = maximum + 1
        entering[tid] = 0
        for i in range(len(tickets)):

                # Wait until thread i receives its number:
            while entering[i]==1:
                 print("waiting on enter")

                # Wait until all threads with smaller numbers or with the samenumber, but with higher priority, finish their work:
            while tickets[i] != 0 and (tickets[tid] > tickets[i] or (tickets[tid] == tickets[i] and tid ) > i):
                #print("")
                continue
        # execute critical section
        print(f"Process {tid} runs a complicated computation!")

        # shows code integrity proof
        print(f"Process {tid} is working!")
        print(f"Process {tid} finished a complicated computation!")
        
        # exit critical section
        tickets[tid] = 0

if __name__ == '__main__':
    DEFAULT_NUM_RUNS = 10
    NUM_THREADS = 6
    threads = [Thread(process, i, DEFAULT_NUM_RUNS) for i in range(NUM_THREADS)]
    [t.join() for t in threads]