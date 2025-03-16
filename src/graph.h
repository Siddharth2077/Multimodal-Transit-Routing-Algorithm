#include "mtra.h"

struct cost;
struct priorityq_entry;

class graph {
private:
    static std::unordered_map<int, node*> nodes;
    static int count;

    // Getters:
    static node* get_node_by_id (const int id);
    static std::vector<int> get_node_ids ();

    // friends
    friend class node;
    friend float euclidean_distance(node *a, node *b);
    friend float euclidean_distance(const int first_node_id, const int second_node_id);

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

struct cost {
    float distance;
    float time;

    cost(float d = 0.0f, float t = 0.0f) : distance(d), time(t) {}
};

// Inline comparator for min-heap behavior
inline cost operator+(const cost& first, const cost& second) {
    return cost(first.distance + second.distance, first.time + second.time);
}

struct priorityq_entry {
    const int current_node_id;
    const int parent_node_id;
    cost *path_cost;

    priorityq_entry(const int c_node_id, const int p_node_id, cost *p_cost) 
        : current_node_id(c_node_id), parent_node_id(p_node_id), path_cost(p_cost) {}

    // Inline comparator for min-heap behavior
    bool operator<(const priorityq_entry &other) const {
        return path_cost->distance < other.path_cost->distance; 
    }
};
