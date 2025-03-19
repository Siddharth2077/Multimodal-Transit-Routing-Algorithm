#include "mtra.h"
#include <Python.h>

int main() {
    // Initialize the Python interpreter
    Py_Initialize();

    // Open the Python file
    FILE* fp = fopen("visualize.py", "r");
    if (fp == nullptr) {
        std::cerr << "Error: Could not open visualize.py" << std::endl;
        Py_Finalize();
        return 1;
    }

    // Execute the script
    int result = PyRun_SimpleFile(fp, "visualize.py");

    // Close the file
    fclose(fp);

    // Finalize the Python interpreter
    Py_Finalize();

    // Check execution status
    if (result == 0) {
        std::cout << "Python script executed successfully." << std::endl;
    } else {
        std::cerr << "Error executing Python script." << std::endl;
    }

    return result;
}








