#pragma once

#include <vector>
#include <iostream>
#include <utility>
#include <memory>
#include <fstream>

using std::enable_shared_from_this;
using std::shared_ptr;
using std::make_shared;
using std::move;

// constant speeds in km/hr
const int WALK_SPEED {4}; 
const int BUS_SPEED {30};
const int METRO_SPEED {50};
const int DRIVE_SPEED {60};

const double EARTH_RADIUS_KM = 6371.0; // Radius of Earth in kilometers

const double PI {3.14159265358979};

const float F_INFINITY {std::numeric_limits<float>().infinity()};

#if defined(_WIN32) || defined(_WIN64)    
    const std::string PATH_ADAPTER {"../"};
#else
    const std::string PATH_ADAPTER {""};
#endif

const std::string PATH_TO_OSM_FILES {PATH_ADAPTER + "../assets/osm_files/"};
const std::string ROAD_NETWORK_TXT_FILE {"road_network.txt"};
const std::string PATH_TXT_FILE {"path.txt"};
const std::string PATH_TO_PYTHON_SCRIPTS {PATH_ADAPTER + "../src/python/"};
const std::string PY_VISUALIZE_SCRIPT {"visualize.py"};
const std::string PY_GENERATE_MAP_SCRIPT {"generate_map.py"};

// Convert degrees to radians
inline double degToRad(double degrees) {
    return degrees * PI / 180.0;
}

#include "node.h"
#include "graph.h"