#pragma once

class node {
private:
    int id;
    float longitude;
    float lattitude;
    static int count;

    node() 
        : longitude(0.0f), lattitude(0.0f), id{++count} {}                      // Default constructor
    node(float lattitude_val, float longitude_val) 
        : lattitude(lattitude_val), longitude(longitude_val), id(++count) {}    // Parameterized Constructor    

};

// Initialize static members
int node::count = 0;
