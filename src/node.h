#pragma once

#include "mtra.h"
#include <unordered_map>

struct path;
struct cost;

class node {
private:
    int id;
    float lattitude;
    float longitude;

    std::unordered_map<int, path> neighbours;

    /// @brief Key: Graph ID | Value: Heuristic value of this node for the graph
    std::unordered_map<int, shared_ptr<cost>> heuristics;          

    // friends
    friend class graph;
    friend float euclidean_distance(node* a, node* b);
    friend float euclidean_distance(const int first_node_id, const int second_node_id);

    node();
    node(float lattitude_val, float longitude_val);
    
    path* calculate_path(const int neighbour_id);

public:
    void print_neighbours ();

    bool add_neighbour (int neighbour_id);

    bool add_neighbour (int neighbour_id, float distance);

    bool add_neighbour(int neighbour_id, const path &path_to_neighbour);

    void print_node ();

    bool add_heuristic (const int graph_id, const int destination_node_id);

    shared_ptr<cost> get_heuristic (const int graph_id);

    std::vector<int> get_neighbour_ids ();
};

struct path {
    float distance = 0.0f;
    float time_walk = 0.0f;
    float time_bus = 0.0f;
    float time_metro = 0.0f;
    float time_drive = 0.0f;
    int popularity = 0;                                                         // Range [0, 10]
};

float euclidean_distance(node* a, node* b);

float euclidean_distance(const int first_node_id, const int second_node_id);