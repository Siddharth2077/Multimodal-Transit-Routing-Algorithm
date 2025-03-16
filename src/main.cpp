#include "mtra.h"
#include <SFML/Graphics.hpp>

int main() {
    graph debug_graph(true);

    sf::RenderWindow window(sf::VideoMode({800, 600}), "Title");
    while (window.isOpen()) {
        // Process events
        while (const std::optional event = window.pollEvent()) {
            // Close window: exit
            if (event->is<sf::Event::Closed>())
                window.close();
        } 
        // Clear screen
        window.clear(); 
        // Update the window
        window.display();
    }

    return 0;
}

