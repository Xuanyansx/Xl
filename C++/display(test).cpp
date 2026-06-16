
#include <iostream>
#include <windows.h>

using namespace std;

int main()
{
    int x = 100;
    int y = 100;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), {x, y});
    cout << "Hello, World!";
    return 0;
}
