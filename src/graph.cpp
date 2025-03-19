#include "mtra.h"
#include <queue>
#include <regex>
#include <fstream>
#include <sstream>
#include <filesystem>

// One Definition Rule
// Header files get imported in multiple files, and will lead to multiple definition of static members
// Static members need to be defined only once, hence, defined in this cpp file to avoid linker errors.
std::unordered_map<long long int, node *> graph::nodes;
int graph::instance_count = 0;

graph::graph() : graph_id(++instance_count) {};

// Constructors:
graph::graph(std::string road_network_txt) : graph_id(++instance_count) {

    std::ifstream road_network_file(road_network_txt); // Ensure this file exists

    if (!road_network_file.is_open()) {
        std::cerr << "ERROR: File '" << road_network_txt << "' does not exist. Exiting..." << std::endl;
        exit(1);
    }
    std::cout << "File: '" << road_network_txt << "' found successfully." << std::endl;

    std::string line;
    bool readingNodes = false;
    bool readingEdges = false;

    while (std::getline(road_network_file, line)) {
        if (line.empty())
            continue;

        if (line == "Nodes:") {
            readingNodes = true;
            readingEdges = false;
            continue;
        }
        else if (line == "Edges:") {
            readingEdges = true;
            readingNodes = false;
            continue;
        }

        if (readingNodes) {
            std::istringstream ss(line);
            std::string nodeId, latLong;

            std::cout.precision(20);

            if (std::getline(ss, nodeId, ':') && std::getline(ss, latLong)) {
                std::istringstream latLongStream(latLong);
                double lattitude, longitude;
                char comma;

                latLongStream >> lattitude >> comma >> longitude;

                node *new_node = new node(stoll(nodeId), lattitude, longitude);
            }
        }
        else if (readingEdges) {
            std::istringstream ss(line);
            std::string node1, arrow, node2;
            if (ss >> node1 >> arrow >> node2 && arrow == "<->") {
                graph::get_node_by_id(std::stoll(node1))->add_neighbour(std::stoll(node2));
                graph::get_node_by_id(std::stoll(node2))->add_neighbour(std::stoll(node1));
            }
        }
    }

    for (auto node_pair : nodes) {
        node_pair.second->print_node();
        node_pair.second->print_neighbours();
    }

    road_network_file.close();
}

graph::graph(bool debug) : graph_id(++instance_count) {
    if (!debug)
        return;
    create_debug_graph();
}

// Destructor
graph::~graph() {
    for (auto &node_pair : nodes) {
        delete node_pair.second;
    }
    nodes.clear();
}

std::vector<long long int> graph::compute_shortest_path(const long long int source_node_id, const long long int destination_node_id) {
    if (!graph::get_node_by_id(source_node_id) || !graph::get_node_by_id(destination_node_id))
        return std::vector<long long int>();

    if (source_node_id == destination_node_id) {
        return {source_node_id};
    }

    bool is_path_found{false};

    // List of Node IDs that comprise the shortest path
    std::vector<long long int> shortest_path{};

    // Key: Node ID | Value: <Parent Node ID, Cost of node ID>
    std::unordered_map<long long int, std::pair<long long int, std::shared_ptr<cost>>> visited;

    struct ComparePriority {
        bool operator()(const std::shared_ptr<priorityq_entry> a, const std::shared_ptr<priorityq_entry> b) const {
            return a->path_cost->distance > b->path_cost->distance; // Min-heap: lower cost has higher priority
        }
    };

    // Priority queue with custom comparator for min-heap
    std::priority_queue<std::shared_ptr<priorityq_entry>, std::vector<std::shared_ptr<priorityq_entry>>, ComparePriority> priority_q;

    node *source_node = graph::get_node_by_id(source_node_id);
    auto source_node_cost = make_shared<cost>(0.0, 0.0);
    source_node->add_heuristic(graph_id, destination_node_id);
    auto source_node_heuristic = source_node->get_heuristic(graph_id);

    auto source_node_entry = make_shared<priorityq_entry>(source_node_id, -1, source_node_cost + source_node_heuristic);
    priority_q.push(source_node_entry);

    visited[source_node_id] = {-1, source_node_cost};

    while (!priority_q.empty()) {

        std::shared_ptr<priorityq_entry> nearest_node_entry = priority_q.top();
        priority_q.pop();

        long long int current_node_id = nearest_node_entry->current_node_id;
        long long int parent_node_id = nearest_node_entry->parent_node_id;

        if (current_node_id == destination_node_id) {
            is_path_found = true;
            break;
        }

        std::vector<long long int> neighbour_ids = graph::get_node_by_id(current_node_id)->get_neighbour_ids();
        for (auto neighbour_id : neighbour_ids) {

            auto neighbour_cost = std::make_shared<cost>(
                visited[current_node_id].second->distance +
                euclidean_distance(current_node_id, neighbour_id) +
                euclidean_distance(neighbour_id, destination_node_id));

            // Checks if we should re-visit this node if it has a lower cost
            if (visited.find(neighbour_id) != visited.end() && visited[neighbour_id].second->distance <= neighbour_cost->distance)
                continue;

            auto q_entry = std::make_shared<priorityq_entry>(neighbour_id, current_node_id, neighbour_cost);
            priority_q.push(q_entry);

            double parent_node_cost = (parent_node_id == -1) ? 0.0 : visited[parent_node_id].second->distance;

            // Store cost in visited using unique_ptr
            visited[neighbour_id] = {
                current_node_id,
                std::make_unique<cost>(parent_node_cost + euclidean_distance(current_node_id, neighbour_id), 0.0)};
        }
    }

    if (!is_path_found) {
        return {};
    }

    shortest_path.push_back(destination_node_id);

    long long int current_node_id = destination_node_id;
    while (visited[current_node_id].first != -1) {
        long long int parent_node_id = visited[current_node_id].first;
        shortest_path.push_back(parent_node_id);
        current_node_id = parent_node_id;
    }

    std::reverse(shortest_path.begin(), shortest_path.end());

    return shortest_path;
}

void graph::create_debug_graph() {
    std::vector<std::pair<int, int>> coordinates = {
        {1, 1}, {1, 4}, {1, 7}, {1, 10}, {2, 5}, {2, 10}, {3, 3}, {3, 6}, {4, 4}, {4, 8}, {6, 2}, {6, 5}, {6, 7}, {7, 9}, {8, 3}, {9, 6}, {9, 8}, {10, 4}, {10, 7}, {11, 2}, {11, 6}, {11, 8}, {12, 4}, {12, 10}, {13, 7}, {13, 9}, {15, 4}};

    for (auto &coordinate : coordinates) {
        node *temp_node = new node(coordinate.first, coordinate.second);
    }

    std::vector<long long int> node_ids = graph::get_node_ids();

    std::vector<std::vector<int>> node_neighbours = {
        {7, 11},
        {3, 5, 7},
        {2, 5, 6, 8},
        {10},
        {2, 3, 8, 9, 15, 16},
        {3, 13, 17},
        {1, 2, 9, 15},
        {3, 5, 9, 10, 13, 19},
        {5, 7, 8, 11, 12, 20},
        {4, 8, 12, 13, 14},
        {1, 9, 20},
        {9, 10, 16, 18},
        {6, 8, 10, 16, 19, 26},
        {10, 16, 17},
        {5, 7, 16, 18, 20, 23},
        {5, 12, 13, 14, 15, 19, 21, 23, 24},
        {6, 14, 22, 24},
        {12, 15, 20, 21},
        {8, 13, 16, 21, 22, 25},
        {9, 11, 15, 18, 23, 27},
        {16, 18, 19, 25, 27},
        {17, 19, 25, 26},
        {15, 16, 20, 27},
        {16, 17, 26},
        {19, 21, 22, 26, 27},
        {13, 22, 24, 25, 27},
        {20, 21, 23, 25, 26}};

    // Build the node neighbours list for each node
    for (int current_node_id{1}; current_node_id <= node_neighbours.size(); current_node_id++) {
        for (auto &neighbour : node_neighbours.at(current_node_id - 1)) {
            if (node *current_node = graph::get_node_by_id(current_node_id)) {
                current_node->add_neighbour(neighbour);
            }
        }
    }
}

void graph::add_to_graph(node *new_node) {
    nodes[new_node->id] = new_node;
}

std::vector<long long int> graph::get_node_ids() {
    std::vector<long long int> node_ids;
    for (const auto &node : nodes)
    {
        node_ids.push_back(node.first);
    }
    return node_ids;
}

node *graph::get_node_by_id(const long long int id) {
    if (nodes.find(id) == nodes.end())
        return nullptr;
    return nodes[id];
}
