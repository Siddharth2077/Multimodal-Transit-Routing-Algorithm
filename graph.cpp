#include "mtra.h"

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
        node temp_node(coordinate.first, coordinate.second);
    }

    std::vector<int> node_ids = node_manager::get_node_ids();

    for (int node_id: node_ids) {
        node_manager::get_node_by_id(node_id)->print_node();
    }

}

graph::graph() = default;

graph::graph (int osm_file) {
    // TODO: Read the osm file and create the graph
}

graph::graph (bool debug) {
    if (!debug)
        return;
    create_debug_graph();
}