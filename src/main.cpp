#include "mtra.h"

int main() {
    
    graph debug_graph(true);

    std::vector<int> shortest_path = debug_graph.compute_shortest_path(1, 27);

    for (int node_id: shortest_path) {
        std::cout<<node_id<<" ";
    }

    std::cout<<std::endl;
    
}
