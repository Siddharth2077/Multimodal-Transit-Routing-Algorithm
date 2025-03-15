#include "mtra.h"

class node_manager {
private:
    node_manager() = default;

    static std::unordered_map<int, shared_ptr<node>> nodes;
    static int count;

public:
    static void add_to_node_manager(node* node);

    static std::vector<int> get_node_ids();

    // TODO: Remove later as we can't allow anyone to modify the node outside node manager
    static shared_ptr<node> get_node_by_id(int id);
};


