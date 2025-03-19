cmake_minimum_required(VERSION 3.10.0)
project(Multimodal-Transit-Routing-Algorithm VERSION 0.1.0 LANGUAGES C CXX)

# Enable C++17 (or newer)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)  # Enforce the standard

# Find Python3
find_package(Python3 COMPONENTS Interpreter Development REQUIRED) 

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")         # --- MacOS Only for M-Series ARM Processors --- #
   set(CMAKE_OSX_ARCHITECTURES "arm64")
endif()

# Recursively compile all our source files from the /src directory
file(GLOB_RECURSE SRC_FILES src/*.cpp src/*.h)

add_executable(${PROJECT_NAME} ${SRC_FILES})

target_link_libraries(
    ${PROJECT_NAME}
    Python3::Python
)
