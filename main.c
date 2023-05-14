#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define N 500
#define D 0.85

int* get_counts_send(int processes_count, int vertices_count) {
    int* sendcounts = (int*)malloc(processes_count * sizeof(int));
    int i;
    double average = ((double) vertices_count) / ((double) processes_count);
    double last = 0.0;
    for (i=0; i < processes_count; i++) {
        sendcounts[i] = ((int) (last + average)) - ((int) last);
        last += average;
    }
    return sendcounts;
}

int* get_displacements(int processes_count, const int* counts_send) {
    int* displs = (int*)malloc(processes_count * sizeof(int));
    int i;
    int j = 0;
    for (i=0; i < processes_count; i++) {
        displs[i] = j;
        j += counts_send[i];
    }
    return displs;
}

void loadMatrixFromFile(const char* filename, int matrix[N][N]) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        printf("Failed to open the file.\n");
        return;
    }

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            fscanf(file, "%1d", &matrix[i][j]);
        }
    }

    fclose(file);

}
int main(int argc, char** argv) {
    // MPI inviroment initialization
    MPI_Init(&argc, &argv);
    int process_id, processes_count;
    MPI_Comm_rank(MPI_COMM_WORLD, &process_id);
    MPI_Comm_size(MPI_COMM_WORLD, &processes_count);
    double start_time, end_time, execution_time;
    start_time = MPI_Wtime();
    double* ranks = NULL;
    int** graph_matrix = NULL;
    int* partitions_counts = NULL;
    int* partitions_indexes = NULL;
    int vertices_count = 0;
    int iterations_count = 0;
    int f, g;

    int matrix[N][N];
    loadMatrixFromFile("input.txt", matrix);
    iterations_count = 100;
    vertices_count = N;
    graph_matrix = (int**)malloc(N * sizeof(int*));
    for (f = 0; f < N; f++)
        graph_matrix[f] = (int*)malloc(N * sizeof(int));
    for (f = 0; f < N; f++)
        for (g = 0; g < N; g++)
            graph_matrix[f][g] = matrix[f][g];


    // Rank array init
    ranks = (double*) malloc(vertices_count * sizeof(double));
    int m;
    for (m = 0; m < vertices_count; m++) {
        ranks[m] = 1.0 / vertices_count;
    }

    // data partition
    partitions_counts = get_counts_send(processes_count, vertices_count);
    partitions_indexes = get_displacements(processes_count, partitions_counts);
    int partition_vertices_count = partitions_counts[process_id];
    int partition_vertex_index = partitions_indexes[process_id];
    double* partition_ranks = (double*)malloc(partition_vertices_count * sizeof(double));
    double* tmp_ranks = (double*)malloc(partition_vertices_count * sizeof(double));
    double tmp_out_links_count;
    int i, j, k, l;

    // Page Rank algorithm iteration
    for (k = 0; k < iterations_count; k++) {

        // MPI Scatter - distribute data to processes
        MPI_Scatterv(ranks, partitions_counts, partitions_indexes, MPI_DOUBLE,
                     partition_ranks, partition_vertices_count, MPI_DOUBLE,
                     0, MPI_COMM_WORLD);

        // PageRank algorithm
        for (i = partition_vertex_index; i < partition_vertex_index + partition_vertices_count; i++) {
            tmp_ranks[i - partition_vertex_index] = 0.0;
            for (j = 0; j < vertices_count; j++) {
                if (graph_matrix[j][i] == 1) {
                    tmp_out_links_count = 0.0;
                    for (l = 0; l < vertices_count; l++) {
                        tmp_out_links_count += graph_matrix[j][l];
                    }
                    tmp_ranks[i - partition_vertex_index] += ranks[j] / tmp_out_links_count;
                }
            }
            partition_ranks[i - partition_vertex_index] = (1.0 - D) + D * tmp_ranks[i - partition_vertex_index];
        }

        // MPI Allgather - accept data from processes
        MPI_Allgatherv(partition_ranks, partition_vertices_count, MPI_DOUBLE,
                       ranks, partitions_counts, partitions_indexes, MPI_DOUBLE,
                       MPI_COMM_WORLD);

    }
    free(partitions_counts);
    free(partitions_indexes);
    free(partition_ranks);
    free(tmp_ranks);


    if (process_id == 0) {
        // Print the final PageRank scores
        for (f = 0; f < N; f++) {
            printf("\nPage %d: %lf\n", f + 1, ranks[f]);
        }
    }

    for (f = 0; f < N; f++)
        free(graph_matrix[f]);
    free(graph_matrix);
    free(ranks);

    end_time = MPI_Wtime(); // Record the ending time

    execution_time = end_time - start_time;

    // Gather execution time from all processes to process 0
    double* all_execution_times = NULL;
    if (process_id == 0) {
        all_execution_times = (double*)malloc(processes_count * sizeof(double));
    }
    MPI_Gather(&execution_time, 1, MPI_DOUBLE, all_execution_times, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // Process 0 prints the execution time
    if (process_id == 0) {
        printf("Execution time: %f seconds\n", execution_time);

        // Additional analysis or processing with the gathered execution times if needed

        free(all_execution_times);
    }
    //Deinitialization of MPI enviroment
        MPI_Finalize();

    return 0;
}
