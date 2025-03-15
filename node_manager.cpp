#include "mtra.h"

// One Definition Rule 
// Header files get imported in multiple files, and will lead to multiple definition of static members
// Static members need to be defined only once, hence, defined in this cpp file to avoid linker errors.
std::unordered_map<int, shared_ptr<node>> node_manager::nodes;
int node_manager::count = 0;

void node_manager::add_to_node_manager(node* new_node) {
    new_node->id = ++count;
    nodes[new_node->id] = make_shared<node>(*new_node);
    std::cout << new_node->id;
}

std::vector<int> node_manager::get_node_ids() {
    std::vector<int> node_ids;
    for (const auto &node : nodes) {
        node_ids.push_back(node.first);
    }
    return node_ids;
}

// TODO: Remove later as we can't allow anyone to modify the node outside node manager
shared_ptr<node> node_manager::get_node_by_id(int id) {
    if (nodes.find(id) == nodes.end())
        return shared_ptr<node>();
    return nodes[id];
}
