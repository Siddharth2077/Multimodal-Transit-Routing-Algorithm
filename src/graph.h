#pragma once

#include "mtra.h"

class graph {
private:
    void create_debug_graph ();

public:
    graph();
    graph (bool debug);
    graph (int osm_file);
};