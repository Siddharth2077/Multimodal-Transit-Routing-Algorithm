#include "mtra.h"

struct cost;
struct priorityq_entry;

class graph {
private:
    static std::unordered_map<long long int, node *> nodes;
    static int instance_count;

    int graph_id{};

    // Getters:
    static node *get_node_by_id(const long long int id);
    static std::vector<long long int> get_node_ids();

    // friends
    friend class node;
    friend double euclidean_distance(node *a, node *b);
    friend double euclidean_distance(const long long int first_node_id, const long long int second_node_id);

    // Helpers:
    void create_debug_graph();

public:
    // Constructors:
    graph();
    graph(bool debug);
    graph(std::string road_network_txt);

    // Destructor
    ~graph();

    // Regular methods:
    std::vector<long long int> compute_shortest_path(const long long int source_node_id, const long long int destination_node_id);

    // Static methods:
    static void add_to_graph(node *node);
};

struct cost {
    double distance;
    double time;

    cost(double d = 0.0f, double t = 0.0f) : distance(d), time(t) {}
};

inline cost operator+(const cost &first, const cost &second) {
    return cost(first.distance + second.distance, first.time + second.time);
}

inline shared_ptr<cost> operator+(const shared_ptr<cost> first, const shared_ptr<cost> second) {
    return make_shared<cost>(first->distance + second->distance, first->time + second->time);
}

struct priorityq_entry {
    const long long int current_node_id;
    const long long int parent_node_id;
    std::shared_ptr<cost> path_cost;

    priorityq_entry(const long long int c_node_id, const long long int p_node_id, std::shared_ptr<cost> p_cost)
        : current_node_id(c_node_id), parent_node_id(p_node_id), path_cost(p_cost) {}
};
