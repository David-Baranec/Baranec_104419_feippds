# Baranec_104419_feippds

Assignment 02: Implement dining philosophers problem

# Introduction 
This problem has many similar definitions. We use this one:

N - philosophers are sitting at a round table. (For this case we care about 5 philosophers).
Each philosopher has a plate in front of him. Each plate has a fork to the left and to the right of it. However, if any 2 philosophers sit next to each other, they share 1 fork as illustrated below, for 
philosopher 0 shares his right fork with philosopher 4.
![img.png](img.png)

Each philosopher behaves independently of other philosophers, but in accordance with the following scenario:
1. Think for some time.
2. Take the right fork.
3. Take the left fork.
4. Eat food.
5. Put the left fork back.
6. Put the right fork back.
Repeat the whole process again, i.e. go to step 1.

If a philosopher wants to take a fork, but this fork is currently used by the neighbor philosopher, 
the philosopher waits until the neighbor puts the fork back before getting it. If two neighbors try to take one fork at the same time, only one of them succeeds and the other one waits.


