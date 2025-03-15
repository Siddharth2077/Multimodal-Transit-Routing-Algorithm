cmake_minimum_required(VERSION 3.10.0)
project(Multimodal-Transit-Routing-Algorithm VERSION 0.1.0 LANGUAGES C CXX)

# Enable C++11 (or newer)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)  # Enforce the standard
set(CMAKE_CXX_EXTENSIONS OFF)        # Disable compiler-specific extensions

add_executable(
    Multimodal-Transit-Routing-Algorithm 
    main.cpp
    node_manager.h
    node_manager.cpp
    node.h
    node.cpp
    graph.h
    graph.cpp
    mtra.h
)

