#include <iostream>
#include <cstdlib>
#include <mpi.h>

using namespace std;

int main(int argc, char** argv) {
    int my_rank, comm_size;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &comm_size);

    // Create a random graph where each node has a random number of followers
    int n = 500;
    int *follower_counts = new int[n];
    for (int i = 0; i < n; i++) {
        follower_counts[i] = 6 + (rand() % n);
    }

    // Compute the sum of follower counts across all nodes
    int my_sum = 0;
    for (int i = my_rank; i < n; i += comm_size) {
        my_sum += follower_counts[i];
    }
    cout << "Process " << my_rank << " computed a sum of " << my_sum << endl;

    // Compute the total sum across all nodes using MPI_Reduce and MPI_Gather
    int total_sum = 0;
    int *gathered_follower_counts = nullptr;
    if (my_rank == 0) {
        gathered_follower_counts = new int[n];
    }
    MPI_Gather(follower_counts, n/comm_size, MPI_INT,
               gathered_follower_counts, n/comm_size, MPI_INT,
               0, MPI_COMM_WORLD);
    MPI_Reduce(&my_sum, &total_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    // Print the total sum on the root process
    if (my_rank == 0) {
        cout << "The total number of followers is " << total_sum << endl;

        // Print the follower count of each node
        cout << "Follower counts:" << endl;
        for (int i = 0; i < n; i++) {
            cout << gathered_follower_counts[i] << " ";
        }
        cout << endl;

        delete[] gathered_follower_counts;
    }

    delete[] follower_counts;
    MPI_Finalize();
    return 0;
}
