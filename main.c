#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <math.h>
#include <time.h>

#define DAMPING_FACTOR 0.85
#define TOLERANCE 0.0001
int cmpfunc(const void *a, const void *b) {
    const double *da = *(const double **)a;
    const double *db = *(const double **)b;
    return (*db > *da) - (*db < *da);
}

void sort_indexes_desc(double *arr, int *idx, int n) {
    double **p = malloc(n * sizeof(double *));
    for (int i = 0; i < n; i++) {
        p[i] = &arr[i];
        idx[i] = i;
    }
    qsort(p, n, sizeof(double *), cmpfunc);
    for (int i = 0; i < n; i++) {
        idx[i] = p[i] - arr;
    }
    free(p);
}

int main(int argc, char** argv) {
    double start_time, end_time, elapsed_time;
    clock_t start_time_total, end_time_total;
    start_time = clock();
    double total_time;
    int my_rank, comm_size;
    int i, j;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &comm_size);
    start_time = MPI_Wtime();
    int n;

    char row[1000];
    int count;
    int my_sum = 0;
    //Control outprint of ranks
    //printf("rank %d out of %d processors\n", my_rank, comm_size);


    // Open the input file for reading
    FILE *input_file = fopen("input.txt", "r");
    if (input_file == NULL) {
        fprintf(stderr, "Error: could not open input file\n");
        exit(1);
    }

    // Read in the number of vertices

    fscanf(input_file, "%d", &n);

// Allocate memory for the follower counts array
    int *follower_counts = (int *) malloc(n * sizeof(int));
    if (follower_counts == NULL) {
        fprintf(stderr, "Error: could not allocate memory\n");
        exit(1);
    }

    // Read in the follower data from the input file and store it in the follower counts array

    for (i = 0; i < n; i++) {
        fscanf(input_file, "%s", row);
        count = 0;
        for (j = 0; j < n; j++) {
            if (row[j] == '1') {
                count++;
            }
        }
        follower_counts[i] = count;
    }

    // Close the input file
    fclose(input_file);

    // Compute the sum of follower counts across all nodes

    for (i = my_rank; i < n; i += comm_size) {
        my_sum += follower_counts[i];
    }

    // Print the number of followers for each vertex
    if (my_rank == 0) {
        printf("Number of followers for each vertex:\n");
        for (i = 0; i < n; i++) {
            printf("Vertex %d: %d\n", i, follower_counts[i]);
        }
    }
    // Compute the total sum across all nodes using MPI_Reduce
    int total_sum = 0;
    MPI_Reduce(&my_sum, &total_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    // Broadcast the total sum to all nodes
    MPI_Bcast(&total_sum, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // Normalize the follower counts to get the initial Page Rank scores
    double *page_rank = (double *) malloc(n * sizeof(double));
    double init_score = 1.0 / n;
    for (i = 0; i < n; i++) {
        page_rank[i] = init_score * follower_counts[i];
    }

    // Iterate until convergence
    int num_iterations = 0;
    double diff = TOLERANCE + 1;
    while (diff > TOLERANCE) {
        // Compute the contribution from incoming edges
        double *incoming_scores = (double *) calloc(n, sizeof(double));
        for (i = my_rank; i < n; i += comm_size) {
            for (j = 0; j < n; j++) {
                if (j != i && follower_counts[j] > 0) {
                    incoming_scores[i] += page_rank[j] / follower_counts[j];
                }
            }
            incoming_scores[i] *= DAMPING_FACTOR;
        }

        // Compute the new Page Rank scores
        double *new_page_rank = (double *) malloc(n * sizeof(double));
        double sum = 0.0;
        for (i = my_rank; i < n; i += comm_size) {
            new_page_rank[i] = incoming_scores[i] + (1 - DAMPING_FACTOR) * init_score;
            sum += new_page_rank[i];
        }

        // Compute the sum of new Page Rank scores across all nodes
        double total_new_score = 0.0;
        MPI_Allreduce(&sum, &total_new_score, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);

        // Compute the difference between the old and new scores
        diff = 0.0;
        for (i = my_rank; i < n; i += comm_size) {
            new_page_rank[i] /= total_new_score;
            diff += fabs(new_page_rank[i] - page_rank[i]);
        }

        // Compute the sum of differences across all nodes
        double total_diff = 0.0;
        MPI_Reduce(&diff, &total_diff, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
        if (my_rank == 0) {
            printf("Iteration %d: difference = %f\n", num_iterations, total_diff);
        }
        // Update the Page Rank scores
        for (i = my_rank; i < n; i += comm_size) {
            page_rank[i] = new_page_rank[i];
        }

        num_iterations++;
        free(incoming_scores);
        free(new_page_rank);
    }
    double fin=0;
    // Print the final Page Rank scores on the root process
    if (my_rank == 0) {
        printf("Page Rank scores:\n");
        for (i = 0; i < n; i++) {
            printf("%f ", page_rank[i]);
            fin+=page_rank[i];
        }
        printf("\n");
        printf("Sum in pageRank %f ", fin);

        int idx[n];

        sort_indexes_desc(page_rank, idx, n);

        printf("\nIndex order in descending order based on value: ");
        for (int i = 0; i < n; i++) {
            printf("%d ", idx[i]);
        }
        printf("\n");
    }

    free(follower_counts);
    free(page_rank);
    end_time = MPI_Wtime();
    elapsed_time = end_time - start_time;

    printf("\nRank %d: Time taken = %f seconds", my_rank, elapsed_time);
    end_time_total = clock(); // Record the ending time
    if (my_rank == 0) {
        total_time =
                ((double) (end_time_total - start_time_total)) / CLOCKS_PER_SEC; // Calculate the total time in seconds
        printf("\nTotal execution time: %f seconds\n", total_time);
    }
    MPI_Finalize();

    return 0;
}

