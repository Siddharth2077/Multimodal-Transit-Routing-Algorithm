#include "mtra.h"

node::node() : longitude(0.0f), lattitude(0.0f), id(0) { // Default constructor
    node_manager::add_to_node_manager(this);
}

node::node (float lattitude_val, float longitude_val)
    : lattitude(lattitude_val), longitude(longitude_val), id(0) { // Parameterized Constructor
    node_manager::add_to_node_manager(this);
}

path* node::calculate_path(const int neighbour_id) {
    if (neighbours.find(neighbour_id) != neighbours.end())
        return nullptr;
    shared_ptr<node> neighbour = node_manager::get_node_by_id(neighbour_id);
    path* path_to_neighbour = new path();
    path_to_neighbour->distance = euclidean_distance(*this, neighbour);
    path_to_neighbour->time_walk = path_to_neighbour->distance / WALK_SPEED;
    path_to_neighbour->time_bus = path_to_neighbour->distance / BUS_SPEED;
    path_to_neighbour->time_metro = path_to_neighbour->distance / METRO_SPEED;
    path_to_neighbour->time_drive = path_to_neighbour->distance / DRIVE_SPEED;
    return path_to_neighbour;
}

void node::print_neighbours() {
    std::cout << "Node " << id << " has the following neighbours:" << std::endl;
    for (auto &neighbour : neighbours) {
        std::cout << "\tNode " << neighbour.first << " with distance " << neighbour.second.distance << std::endl;
    }
}

bool node::add_neighbour (int neighbour_id) {
    if (neighbours.find(neighbour_id) != neighbours.end())
        return false;
    // Null check
    if (path* path_to_neighbour = calculate_path(neighbour_id)) {
        neighbours[neighbour_id] = *path_to_neighbour;
        return true;
    }
    return false;
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

float euclidean_distance(node &a, shared_ptr<node> b) {
    return sqrt(pow(a.longitude - b->longitude, 2) + pow(a.lattitude - b->lattitude, 2));
}