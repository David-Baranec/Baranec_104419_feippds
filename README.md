# Baranec_104419_feippds

Assignment 01: Implement Bakery algorithm and explain why it is the most suitable method of mutual exclusion.

# General explanation: 
Bakery algorithm explanation: 
This algorithm is known as the bakery algorithm as this type of scheduling is adopted in bakeries where token numbers are issued to set the order of customers. 
When a customer enters a bakery store, he gets a unique token number on its entry. 
The global counter displays the number of customers currently being served, 
and all other customers must wait at that time. Once the baker finishes serving the current customer, 
the next number is displayed. The customer with the next token is now being served.

# Solution: 
When a process wishes to enter a critical section, it chooses a greater token number than any earlier number.

Consider a process Pi wishes to enter a critical section, it sets entering[i] to true to make other processes aware that it is choosing a token number. 
It then chooses a token number greater than those held by other processes and writes its token number. 
Then it sets entering[i] to false after reading them. Then It enters a loop to evaluate the status of other processes. 
It waits until some other process Pj is choosing its token number.

When the process has finished with its critical section execution, it resets its number variable to 0.

