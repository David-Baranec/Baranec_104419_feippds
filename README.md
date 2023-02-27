# Baranec_104419_feippds

Assignment 01: Implement Bakery algorithm and explain why it is the most suitable method of mutual exclusion.

# General explanation: 
Bakery algorithm explanation: 
This algorithm is known as the bakery algorithm as this type of scheduling is adopted in bakeries where token numbers are issued to set the order of customers. 
When a customer enters a bakery store, he gets a unique token number on its entry. 
The global counter displays the number of customers currently being served, 
and all other customers must wait at that time. Once the baker finishes serving the current customer, 
the next number is displayed. The customer with the next token is now being served.

# To run
To run this program just run main. In main are set 10 start with 6 threads by default. This params can be modified up on our wish.

# Solution: 
When a process wishes to enter a critical section, it chooses a greater token number than any earlier number.

Consider a process Pi wishes to enter a critical section, it sets entering[i] to true to make other processes aware that it is choosing a token number. 
It then chooses a token number greater than those held by other processes and writes its token number. 
Then it sets entering[i] to false after reading them. Then It enters a loop to evaluate the status of other processes. 
It waits until some other process Pj is choosing its token number.

When the process has finished with its critical section execution, it resets its number variable to 0.

# Explanation: Bakery algorithm is correct solution of mutual exclusion 
Mutual Exclusion: we know that when no process is executing in its critical section, a process with the lowest number is allowed to enter its critical section. 
Suppose two processes have the same token number. In that case, the process with the lower process ID among these is selected as the process ID of each process is distinct,
so at a particular time, there will be only one process executing in its critical section. 
Thus the requirement of mutual Exclusion is met.

Bounded Waiting: As awaiting, the process will enter its critical section when no other process is in its critical section and
If its token number is the smallest among other waiting processes.
If token numbers are the same, it has the lowest process ID among other waiting processes.

Progress: After selecting a token, a waiting process checks whether any other waiting process has higher priority to enter its critical section. 
If there is no such process, P will immediately enter its critical section. Thus meeting progress requirements.