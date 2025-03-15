#pragma once

#include <vector>

class graph;
struct path;

class node {
private:
    int id;
    float longitude;
    float lattitude;
    static int count;
    std::vector<std::vector<node*, path>> paths;

    friend graph;

    friend float euclidean_distance(node& a, node& b);

    node() 
        : longitude(0.0f), lattitude(0.0f), id{++count} {}                      // Default constructor
    node(float lattitude_val, float longitude_val) 
        : lattitude(lattitude_val), longitude(longitude_val), id(++count) {}    // Parameterized Constructor    

};

// Initialize static members
int node::count = 0;

struct path
{
    float distance = 0.0f;
    float time_walk = 0.0f;
    float time_bus = 0.0f;
    float time_metro = 0.0f;
    float time_drive = 0.0f;
    int popularity = 0;                                                         // Range [0, 10]
};

float euclidean_distance(node& a, node& b) {
    return sqrt(pow(a.longitude - b.longitude, 2) + pow(a.lattitude - b.lattitude, 2));
}
