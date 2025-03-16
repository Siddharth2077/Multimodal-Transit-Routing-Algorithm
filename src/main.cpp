#include <SFML/Graphics.hpp>
#include <vector>
#include <iostream>

// Window settings
const int WIDTH = 800, HEIGHT = 600;
const int GRID_SPACING = 50;  // Distance between grid lines
const sf::Vector2f ORIGIN(WIDTH / 2, HEIGHT / 2);  // Center of the window

// Converts logical coordinates (cartesian) to screen coordinates
sf::Vector2f toScreenCoords(float x, float y) {
    return { ORIGIN.x + x, ORIGIN.y - y };
}

int main() {
    sf::RenderWindow window(sf::VideoMode(WIDTH, HEIGHT), "Graph Plotter - SFML 2.6.2");
    window.setFramerateLimit(60);

    // Sample points to plot (adjust these as needed)
    std::vector<sf::Vector2f> points = { {-100, 100}, {50, -50}, {200, 150}, {-150, -100} };

    const std::string fontpath {"../../assets/fonts/Roboto-Medium.ttf"};

    // Load font for labels
    sf::Font font;
    if (!font.loadFromFile(fontpath)) {
        std::cerr << "Error loading font!" << std::endl;
        return -1;
    }

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear(sf::Color::White);

        // Draw grid lines
        sf::Color gridColor(200, 200, 200);  // Light gray

        for (int x = 0; x < WIDTH / 2; x += GRID_SPACING) {
            // Vertical grid lines (right & left)
            sf::Vertex vline[] = {
                sf::Vertex(toScreenCoords(x, -HEIGHT / 2), gridColor),
                sf::Vertex(toScreenCoords(x, HEIGHT / 2), gridColor)
            };
            sf::Vertex vline_neg[] = {
                sf::Vertex(toScreenCoords(-x, -HEIGHT / 2), gridColor),
                sf::Vertex(toScreenCoords(-x, HEIGHT / 2), gridColor)
            };
            window.draw(vline, 2, sf::Lines);
            window.draw(vline_neg, 2, sf::Lines);
        }

        for (int y = 0; y < HEIGHT / 2; y += GRID_SPACING) {
            // Horizontal grid lines (top & bottom)
            sf::Vertex hline[] = {
                sf::Vertex(toScreenCoords(-WIDTH / 2, y), gridColor),
                sf::Vertex(toScreenCoords(WIDTH / 2, y), gridColor)
            };
            sf::Vertex hline_neg[] = {
                sf::Vertex(toScreenCoords(-WIDTH / 2, -y), gridColor),
                sf::Vertex(toScreenCoords(WIDTH / 2, -y), gridColor)
            };
            window.draw(hline, 2, sf::Lines);
            window.draw(hline_neg, 2, sf::Lines);
        }

        // Draw X and Y axes (bold black)
        sf::Vertex xAxis[] = {
            sf::Vertex(toScreenCoords(-WIDTH / 2, 0), sf::Color::Black),
            sf::Vertex(toScreenCoords(WIDTH / 2, 0), sf::Color::Black)
        };
        sf::Vertex yAxis[] = {
            sf::Vertex(toScreenCoords(0, -HEIGHT / 2), sf::Color::Black),
            sf::Vertex(toScreenCoords(0, HEIGHT / 2), sf::Color::Black)
        };
        window.draw(xAxis, 2, sf::Lines);
        window.draw(yAxis, 2, sf::Lines);

        // Draw points with labels
        sf::Color pointColor = sf::Color::Red;
        float radius = 15.f;  // Increased size for better visibility
        int pointIndex = 1;

        for (const auto& point : points) {
            sf::Vector2f screenPos = toScreenCoords(point.x, point.y);

            // Draw circle
            sf::CircleShape dot(radius);
            dot.setPosition(screenPos.x - radius, screenPos.y - radius);
            dot.setFillColor(pointColor);
            window.draw(dot);

            // Draw number inside circle
            sf::Text label;
            label.setFont(font);
            label.setString(std::to_string(pointIndex));
            label.setCharacterSize(14);
            label.setFillColor(sf::Color::White);
            label.setStyle(sf::Text::Bold);

            // Center the text inside the circle
            sf::FloatRect textBounds = label.getLocalBounds();
            label.setOrigin(textBounds.width / 2, textBounds.height / 2);
            label.setPosition(screenPos.x, screenPos.y - 3);  // Adjust to center

            window.draw(label);
            pointIndex++;
        }

        window.display();
    }

    return 0;
}
