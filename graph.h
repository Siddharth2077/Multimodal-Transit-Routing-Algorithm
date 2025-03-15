#pragma once

#include <vector>
#include "node.h"

class graph {
private:
    std::vector<std::vector<node*>> adj_list;

    graph() = default;

    graph (int osm_file) {
        // TODO: Read the osm file and create the graph
    }



    graph (bool debug) {
        if (!debug) 
            return;
        
        


    }




public:



};