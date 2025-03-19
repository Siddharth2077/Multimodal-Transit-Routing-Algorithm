#include "mtra.h"

long long int node::node_count = 0;

node::node() : longitude(0.0f), lattitude(0.0f), id(++node_count)
{ // Default constructor
    graph::add_to_graph(this);
}

node::node(double lattitude_val, double longitude_val)
{ // Optional Value Constructor
    // Constructor chaining
    node(++node_count, lattitude_val, longitude_val);
}

node::node(long long int id_value, double lattitude_val, double longitude_val)
    : id(id_value), lattitude(lattitude_val), longitude(longitude_val)
{ // All Parameters Constructor
    graph::add_to_graph(this);
}

path *node::calculate_path(const long long int neighbour_id)
{
    if (neighbours.find(neighbour_id) != neighbours.end())
        return nullptr;
    node *neighbour = graph::get_node_by_id(neighbour_id);
    path *path_to_neighbour = new path();
    path_to_neighbour->distance = euclidean_distance(this, neighbour);
    path_to_neighbour->time_walk = path_to_neighbour->distance / WALK_SPEED;
    path_to_neighbour->time_bus = path_to_neighbour->distance / BUS_SPEED;
    path_to_neighbour->time_metro = path_to_neighbour->distance / METRO_SPEED;
    path_to_neighbour->time_drive = path_to_neighbour->distance / DRIVE_SPEED;
    return path_to_neighbour;
}

void node::print_neighbours()
{
    std::cout << "Node " << id << " has the following neighbours:" << std::endl;
    for (auto &neighbour : neighbours)
    {
        std::cout << "\tNode " << neighbour.first << " with distance " << neighbour.second.distance << std::endl;
    }
}

bool node::add_neighbour(long long int neighbour_id)
{
    if (neighbours.find(neighbour_id) != neighbours.end())
        return false;
    // Null check
    if (path *path_to_neighbour = calculate_path(neighbour_id))
    {
        neighbours[neighbour_id] = *path_to_neighbour;
        return true;
    }
    return false;
}

bool node::add_neighbour(long long int neighbour_id, const path &path_to_neighbour)
{
    if (neighbours.find(neighbour_id) != neighbours.end())
        return false;
    neighbours[neighbour_id] = path_to_neighbour;
    return true;
}

std::vector<long long int> node::get_neighbour_ids()
{
    std::vector<long long int> node_neighbours{};
    for (auto &neighbour : neighbours)
    {
        node_neighbours.push_back(neighbour.first);
    }
    return node_neighbours;
}

void node::print_node()
{
    std::cout << "Node id: " << id << " Lattitude: " << lattitude << " Longitude: " << longitude << std::endl;
}

bool node::add_heuristic(const int graph_id, const long long int destination_node_id)
{
    if (!graph::get_node_by_id(destination_node_id))
        return false;
    heuristics[graph_id] = make_shared<cost>(euclidean_distance(id, destination_node_id), 0.0f);
    return true;
}

shared_ptr<cost> node::get_heuristic(const int graph_id)
{
    if (heuristics.find(graph_id) == heuristics.end())
        return shared_ptr<cost>();
    return heuristics[graph_id];
}

// Friend functions:
double euclidean_distance(node *a, node *b)
{
    if (!a || !b)
        return F_INFINITY;

    return sqrt(pow(a->longitude - b->longitude, 2) + pow(a->lattitude - b->lattitude, 2));
}

double euclidean_distance(const long long int first_node_id, const long long int second_node_id)
{
    node *first_node = graph::get_node_by_id(first_node_id);
    node *second_node = graph::get_node_by_id(second_node_id);
    return euclidean_distance(first_node, second_node);
}