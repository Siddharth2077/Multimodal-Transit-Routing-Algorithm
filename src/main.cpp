#include "mtra.h"
#include <Python.h>

int main()
{

    std::string road_network_txt = PATH_TO_OSM_FILES + "/" + ROAD_NETWORK_TXT_FILE;
    graph test_graph(road_network_txt);

    // Initialize the Python interpreter
    // Py_Initialize();

    // // // Open the Python file
    // // FILE* fp;
    // // errno_t err = fopen(&fp, "../src/python/plot_graph.py", "r");
    // // if (err != 0 || fp == nullptr) {
    // //     std::cerr << "Error: Could not open visualize.py" << std::endl;
    // //     Py_Finalize();
    // //     return 1;
    // // }

    // // Open the Python file
    // FILE *fp = fopen("../src/python/plot_graph.py", "r");
    // if (!fp)
    // {
    //     perror("Error opening file");
    //     Py_Finalize();
    //     return 1;
    // }

    // // Execute the script
    // int result = PyRun_SimpleFile(fp, "visualize.py");

    // // Close the file
    // fclose(fp);

    // // Finalize the Python interpreter
    // Py_Finalize();

    // // Check execution status
    // if (result == 0) {
    //     std::cout << "Python script executed successfully." << std::endl;
    // } else {
    //     std::cerr << "Error executing Python script." << std::endl;
    // }
}
