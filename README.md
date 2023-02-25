# Baranec_104419_feippds

Assignment 01: Implement Bakery algorithm and explain why it is the most suitable method of mutual exclusion.

# General explanation: 
Bakery algorithm explanation: 
This algorithm is known as the bakery algorithm as this type of scheduling is adopted in bakeries where token numbers are issued to set the order of customers. 
When a customer enters a bakery store, he gets a unique token number on its entry. 
The global counter displays the number of customers currently being served, 
and all other customers must wait at that time. Once the baker finishes serving the current customer, 
the next number is displayed. The customer with the next token is now being served.

