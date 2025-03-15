#include "mtra.h"

node::node() : longitude(0.0f), lattitude(0.0f), id(0) { // Default constructor
    node_manager::add_to_node_manager(this);
}

node::node (float lattitude_val, float longitude_val)
    : lattitude(lattitude_val), longitude(longitude_val), id(0) { // Parameterized Constructor
    node_manager::add_to_node_manager(this);
}

void node::print_neighbours() {
    std::cout << "Node " << id << " has the following neighbours:" << std::endl;
    for (auto &neighbour : neighbours) {
        std::cout << "\tNode " << neighbour.first << " with distance " << neighbour.second.distance << std::endl;
    }
}

bool node::add_neighbour(int neighbour_id, float distance) {
    if (neighbours.find(neighbour_id) != neighbours.end())
        return false;
    path path_to_neighbour;
    path_to_neighbour.distance = distance;
    neighbours[neighbour_id] = path_to_neighbour;
    return true;
}

bool node::add_neighbour(int neighbour_id, const path &path_to_neighbour) {
    if (neighbours.find(neighbour_id) != neighbours.end())
        return false;
    neighbours[neighbour_id] = path_to_neighbour;
    return true;
}

void node::print_node() {
    std::cout << "Node id: " << id << " Lattitude: " << lattitude << " Longitude: " << longitude << std::endl;
}

float euclidean_distance(node &a, node &b) {
    return sqrt(pow(a.longitude - b.longitude, 2) + pow(a.lattitude - b.lattitude, 2));
}