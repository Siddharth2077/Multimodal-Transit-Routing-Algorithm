#pragma once

#include "mtra.h"
#include <unordered_map>

struct path;
struct cost;

class node {
private:
    long long int id;
    double lattitude;
    double longitude;

    static long long int node_count;
    static long long int DEBUG_COUNTER;

    std::unordered_map<long long int, path> neighbours;

    /// @brief Key: Graph ID | Value: Heuristic value of this node for the graph
    std::unordered_map<int, shared_ptr<cost>> heuristics;

    // friends
    friend class graph;
    friend double euclidean_distance(node *a, node *b);
    friend double euclidean_distance(const long long int first_node_id, const long long int second_node_id);
    friend double coordinates_euclidean_distance(double lat1, double lon1, double lat2, double lon2);

    node();
    node(double lattitude_val, double longitude_val);
    node(long long int id_value, double lattitude_val, double longitude_val);

    path *calculate_path(const long long int neighbour_id);

public:
    void print_neighbours();

    bool add_neighbour(long long int neighbour_id);

    bool add_neighbour(long long int neighbour_id, double distance);

    bool add_neighbour(long long int neighbour_id, const path &path_to_neighbour);

    void print_node();

    bool add_heuristic(const int graph_id, const long long int destination_node_id);

    shared_ptr<cost> get_heuristic(const int graph_id);

    std::vector<long long int> get_neighbour_ids();
};

struct path {
    double distance = 0.0;
    double time_walk = 0.0;
    double time_bus = 0.0;
    double time_metro = 0.0;
    double time_drive = 0.0;
    int popularity = 0; // Range [0, 10]
};

double euclidean_distance(node *a, node *b);

double euclidean_distance(const long long int first_node_id, const long long int second_node_id);

// Function to compute coordinates Euclidean distance (approximated)
double coordinates_euclidean_distance(double lat1, double lon1, double lat2, double lon2);