#include "mtra.h"
#include <Python.h>

int main() {

    // // Initialize the Python interpreter
    // Py_Initialize();

    // // Open the Python file
    // FILE *fp = fopen((PATH_TO_PYTHON_SCRIPTS + PY_GENERATE_MAP_SCRIPT).c_str(), "r");
    // if (fp == nullptr) {
    //     std::cerr << "Error: Could not open generate_map.py" << std::endl;
    //     Py_Finalize();
    //     return 1;
    // }

    // // Execute the script
    // PyRun_SimpleFile(fp, PY_GENERATE_MAP_SCRIPT.c_str());

    // // Close the file
    // fclose(fp);

    // std::string road_network_txt = PATH_TO_OSM_FILES + ROAD_NETWORK_TXT_FILE;
    // graph test_graph(road_network_txt);

    // std::vector<long long int> path = test_graph.compute_shortest_path(246463900, 10926590269);

    // std::string path_txt = PATH_TO_OSM_FILES + PATH_TXT_FILE;
    // std::ofstream outFile(path_txt); 
    // if (!outFile) {
    //     std::cerr << "Error opening file: " << path_txt << std::endl;
    //     return 1; 
    // }
    // for (long long int node : path) {
    //     outFile << node << std::endl; 
    // }
    // outFile.close();

    // // Open the Python file
    // FILE* vp = fopen((PATH_TO_PYTHON_SCRIPTS + PY_VISUALIZE_SCRIPT).c_str(), "r");
    // if (vp == nullptr) {
    //     std::cerr << "Error: Could not open visualize.py" << std::endl;
    //     Py_Finalize();
    //     return 1;   
    // }

    // // Execute the script
    // PyRun_SimpleFile(vp, PY_VISUALIZE_SCRIPT.c_str());

    // // Close the file
    // fclose(vp);

    // // Finalize the Python interpreter
    // Py_Finalize();

    // Initialize the Python interpreter
    Py_Initialize();

    // Open the Python file
    FILE *fp = fopen((PATH_TO_PYTHON_SCRIPTS + PY_VISUALIZE_STOPS_SCRIPT).c_str(), "r");
    if (fp == nullptr) {
        std::cerr << "Error: Could not open visualize_stops.py" << std::endl;
        Py_Finalize();
        return 1;
    }

    // Execute the script
    PyRun_SimpleFile(fp, PY_VISUALIZE_STOPS_SCRIPT.c_str());

    // Close the file
    fclose(fp);

    // Finalize the Python interpreter
    Py_Finalize();
}
