#include "mtra.h"

class graph {
private:
    static std::unordered_map<int, node*> nodes;
    static int count;

    // Getters:
    static node* get_node_by_id (const int id);
    static std::vector<int> get_node_ids ();

    // friends
    friend class node;

    // Helpers:
    void create_debug_graph ();

public:
    // Constructors:
    graph ();
    graph (bool debug);
    graph (int osm_file);

    // Destructor
    ~graph();

    // Regular methods:
    std::vector<int> compute_shortest_path (const int source_node_id, const int destination_node_id);

    // Static methods:
    static void add_to_graph (node* node);    
};


