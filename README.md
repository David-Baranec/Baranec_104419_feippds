# Baranec_104419_feippds

Assignment 02: Implement Sleeping Barber Problem with overtaking

# Introduction 
Dijkstra introduced the sleeping barber problem in 1965. This problem is based on a hypothetical scenario where there is a barbershop with one barber. The barbershop is divided into two rooms, the waiting room, and the workroom. The waiting room has n chairs for waiting customers, and the workroom only has a barber chair.

Now, if there is no customer, then the barber sleeps in his own chair(barber chair). Whenever a customer arrives, he has to wake up the barber to get his haircut. If there are multiple customers and the barber is cutting a customer's hair, then the remaining customers wait in the waiting room with "n" chairs(if there are empty chairs), or they leave if there are no empty chairs in the waiting room.

The sleeping barber problem may lead to a race condition. This problem has occurred because of the actions of both barber and customer.

# Solution
The following solution uses five semaphores, one for customer(for counts of waiting for customers), one for barber(a binary semaphore denoting the state of the barber, i.e., 0 for idle and 1 for busy), these 2 are for deal of starting the hair cutting. Third one is for "customer_done" state and "barber_done" state which are used for synchronization. 
They ensure that the next customer can only get to the waiting room when the current customer is cut and. Lastly there is a mutual exclusion semaphore, mutex for seats (protects integrity of counter).

# Console output
![img.png](img.png)
