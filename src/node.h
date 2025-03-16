#pragma once

#include "mtra.h"
#include <unordered_map>

struct path;

class node {
private:
    int id;
    float lattitude;
    float longitude;
    std::unordered_map<int, path> neighbours;
    std::unordered_map<int, float> heuristics;

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

    std::vector<int> get_neighbour_ids ();

    void print_node ();
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