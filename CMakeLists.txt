cmake_minimum_required(VERSION 3.10.0)
project(Multimodal-Transit-Routing-Algorithm VERSION 0.1.0 LANGUAGES C CXX)

# Enable C++17 (or newer)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)  # Enforce the standard
set(CMAKE_CXX_EXTENSIONS OFF)        # Disable compiler-specific extensions

if(CMAKE_SYSTEM_NAME STREQUAL "Windows")            # --------------------------- WINDOWS --------------------------- #
    # Add include directories
    include_directories(${CMAKE_SOURCE_DIR}/include)
    # SFML include directories
    include_directories("D:/My Documents/C++ Projects/libraries/SFML-3.0.0/include")

    # Manually link SFML libraries
    set(SFML_LIB_DIR "D:/My Documents/C++ Projects/libraries/SFML-3.0.0/lib")
    link_directories(${SFML_LIB_DIR})

    # Set SFML Cmake directory
    set(SFML_DIR "D:/My Documents/C++ Projects/libraries/SFML-3.0.0/lib/cmake/SFML")

    # Recursively compile all our source files from the /src directory
    file(GLOB_RECURSE SRC_FILES src/*.cpp src/*.h)

    # Add all the source files under /src
    add_executable(Multimodal-Transit-Routing-Algorithm ${SRC_FILES})

    # Link SFML libraries
    target_link_libraries(
        Multimodal-Transit-Routing-Algorithm 
        "${SFML_LIB_DIR}/sfml-graphics.lib"
        "${SFML_LIB_DIR}/sfml-window.lib"
        "${SFML_LIB_DIR}/sfml-audio.lib"
        "${SFML_LIB_DIR}/sfml-network.lib"
        "${SFML_LIB_DIR}/sfml-system.lib"  # You can keep this here manually
        opengl32
        winmm
        gdi32
        user32
        freetype
    )   

elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")         # ---------------------------- MacOS ---------------------------- #


endif()

