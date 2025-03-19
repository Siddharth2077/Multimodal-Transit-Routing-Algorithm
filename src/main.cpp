#include "mtra.h"
#include <Python.h>

int main() {

    // std::string road_network_txt = PATH_TO_OSM_FILES + ROAD_NETWORK_TXT_FILE;
    // graph test_graph(road_network_txt);

    // Initialize the Python interpreter
    Py_Initialize();

    // Open the Python file
    FILE* fp = fopen((PATH_TO_PYTHON_SCRIPTS + PY_VISUALIZE_SCRIPT).c_str(), "r");
    if (fp == nullptr) {
        std::cerr << "Error: Could not open visualize.py" << std::endl;
        Py_Finalize();
        return 1;   
    }

    // Execute the script
    PyRun_SimpleFile(fp, PY_VISUALIZE_SCRIPT.c_str());

    // Close the file
    fclose(fp);

    // Finalize the Python interpreter
    Py_Finalize();
}
