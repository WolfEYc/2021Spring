#include <SFML/Graphics.hpp>
#include <iostream>

//to compile & run
// g++ main.cpp -o butterslide -lsfml-graphics -lsfml-window -lsfml-system && ./butterslide
int main()
{
    // create the window
    

    sf::RenderWindow window(sf::VideoMode(800, 600), "My window",sf::Style::Close);
    window.setKeyRepeatEnabled(false);
    // run the program as long as the window is open
    while (window.isOpen())
    {
        // check all the window's events that were triggered since the last iteration of the loop
        sf::Event event;
        while (window.pollEvent(event))
        {
            
            // "close requested" event: we close the window
            if (event.type == sf::Event::Closed)
                window.close();
            
            if(event.type == sf::Event::KeyPressed){
                if(event.key.code == sf::Keyboard::Right){
                    //std::cout<<"right key pressed"<<std::endl;
                }
                if(event.key.code == sf::Keyboard::Left){
                    //std::cout<<"right key pressed"<<std::endl;
                }
            }
            if(event.type == sf::Event::KeyReleased){
                if(event.key.code == sf::Keyboard::Right){
                    //std::cout<<"right key pressed"<<std::endl;
                }
                if(event.key.code == sf::Keyboard::Left){
                    //std::cout<<"right key pressed"<<std::endl;
                }
            }
        }

        // clear the window with black color
        window.clear(sf::Color::Black);

        // draw everything here...
        // window.draw(...);

        // end the current frame
        window.display();
    }

    return 0;
}