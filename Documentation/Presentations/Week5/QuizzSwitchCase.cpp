#include <iostream>

enum Color {
    RED,
    GREEN,
    BLUE
};

void execute()
{
    char var[10000000];
    int a = 3;
    a++;
}

int main() {
    Color color = RED;
    {
        int a =3;
    }
    execute();
    switch (color) {
    case RED:
    {
        int redValue;  // Declaration without braces
        redValue = 255;
        std::cout << "Red intensity: " << redValue << std::endl;
        break;
    }
    case GREEN:
        // Correct use with braces
        {
            int greenValue = 128;
            std::cout << "Green intensity: " << greenValue << std::endl;
        }
        break;
    case BLUE:
        // Correct use with braces
        {
            int blueValue = 100;
            std::cout << "Blue intensity: " << blueValue << std::endl;
        }
        break;
    }

    return 0;
}
