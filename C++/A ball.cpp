#include <iostream>
#include <stdio.h>
#include <string>
#include <windows.h>
#include <time.h>
#define g 10

using namespace std;

const char* input(const char* str)
{
    char* res = (char*)malloc(64 * sizeof(char));
    printf("%s", str);
    scanf("%63s", res); // 限制输入长度
    return res;
}



// class Ball {
//     public:
//         int x,y,radius;
    
//         Ball(int x,int y,int radius){
//             this->x = x;
//             this->y = y;
//             this->radius = radius;
//         }

// };

struct POS
{
    int x;
    int y;
};


void gotoYX( int y, int x ) {
    COORD c;
    c.X = x;
    c.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE),c);
}

// void display(POS pos,string *buffer){
//     gotoXY(pos.x,pos.y);
//     fputs((*buffer).c_str(),stdout);


// }


void move(POS pos,int speed,int direction){
    // 180 <=direction <= 0

}

int main(){
    int x = 0;
    int y = 0;

    // int speed = atoi(input("输入球的速度 :"));
    HANDLE h = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_CURSOR_INFO cursorInfo;
    GetConsoleCursorInfo(h, &cursorInfo);
    cursorInfo.bVisible = false;
    SetConsoleCursorInfo(h, &cursorInfo);

    for (int i = 0; i < 10; i++)
    {
        y = y+1;

        for(int j = 0;j<2;j++){
            x= x+1;
            gotoYX(y,x);
            printf("@");
        }
        // x = i+dx;
        // y = 4+dy;

        Sleep(100);
    }
    getchar();
    getchar();


    return 0;
}