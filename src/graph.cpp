#include "mtra.h"

// One Definition Rule 
// Header files get imported in multiple files, and will lead to multiple definition of static members
// Static members need to be defined only once, hence, defined in this cpp file to avoid linker errors.
std::unordered_map<int, node*> graph::nodes;
int graph::count = 0;

// Constructors:
graph::graph() = default;

graph::graph (int osm_file) {
    // TODO: Read the osm file and create the graph
}

graph::graph (bool debug) {
    if (!debug)
        return;
    create_debug_graph();
}

// Destructor
graph::~graph()  {
    for (auto& node_pair : nodes) {
        delete node_pair.second;
    }
    nodes.clear();
}

std::vector<int> graph::compute_shortest_path (const int source_node_id, const int destination_node_id) {
    if (!graph::get_node_by_id(source_node_id) || !graph::get_node_by_id(destination_node_id))
        return std::vector<int>();

    std::vector<int> shortest_path{};
    
    return shortest_path;
}

void graph::create_debug_graph () {
    std::vector<std::pair<int, int>> coordinates = {
        {1, 1}, {1, 4}, {1, 7}, {1, 10},
        {2, 5}, {2, 10},
        {3, 3}, {3, 6},
        {4, 4}, {4, 8},
        {6, 2}, {6, 5}, {6, 7},
        {7, 9},
        {8, 3},
        {9, 6}, {9, 8},
        {10, 4}, {10, 7}, 
        {11, 2}, {11, 6}, {11, 8},
        {12, 4}, {12, 10},
        {13, 7}, {13, 9},
        {15, 4}
    };

    for (auto &coordinate: coordinates) {
        node* temp_node = new node(coordinate.first, coordinate.second);
    }

    std::vector<int> node_ids = graph::get_node_ids();

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
        {20, 21, 23, 25, 26}
    };

    // Build the node neighbours list for each node
    for (int current_node_id{1}; current_node_id <= node_neighbours.size(); current_node_id++) {
        for (auto& neighbour: node_neighbours.at(current_node_id - 1)) {
            if (node* current_node = graph::get_node_by_id(current_node_id)) {
                current_node->add_neighbour(neighbour);
            }            
        }
    }

    for (int node_id: node_ids) {
        graph::get_node_by_id(node_id)->print_neighbours();
    }

}

void graph::add_to_graph(node* new_node) {
    new_node->id = ++count;
    nodes[new_node->id] = new_node;
}

std::vector<int> graph::get_node_ids() {
    std::vector<int> node_ids;
    for (const auto &node : nodes) {
        node_ids.push_back(node.first);
    }
    return node_ids;
}

node* graph::get_node_by_id(const int id) {
    if (nodes.find(id) == nodes.end())
        return nullptr;
    return nodes[id];
}
