#pragma once

#include <vector>
#include <iostream>
#include <utility>
#include <memory>

using std::enable_shared_from_this;
using std::shared_ptr;
using std::make_shared;
using std::move;

// constant speeds in km/hr
const int WALK_SPEED {4}; 
const int BUS_SPEED {30};
const int METRO_SPEED {50};
const int DRIVE_SPEED {60};

const float F_INFINITY {std::numeric_limits<float>().infinity()};

#if defined(_WIN32) || defined(_WIN64)
    const std::string PATH_TO_OSM_FILES {"../../assets/osm_files"};
#else
    const std::string PATH_TO_OSM_FILES {"../assets/osm_files"};
#endif
const std::string ROAD_NETWORK_TXT_FILE {"road_network.txt"};

#include "node.h"
#include "graph.h"