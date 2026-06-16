#include <stdio.h>
#include <iostream>
#include <vector>
#include <time.h>
#include "screen.h"
#include <windows.h>
#include <string.h>
#include <cmath>
using namespace std;
// void Screen::FillScreenWithString(const char *frame) {
//     COORD coord = {0, 0};
//     SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
//     fputs(frame,stdout);
// }
// int Find(vector<int> vec,int key){
//     int res = -1;

//     for (int i = 0;i<vec.size();i++){
//         if (vec[i] == key){
//             res = i;
//             break;
//         }

//     }

//     return res;

// }
int getRandomInt(int min, int max)
{ // ai生成的，这个我不咋会用
    // 使用当前时间作为种子，只需要在程序初始化时调用一次
    static bool seedInitialized = false;
    if (!seedInitialized)
    {
        srand(static_cast<unsigned>(time(nullptr)));
        seedInitialized = true;
    }

    // 生成随机整数
    int randomValue = min + rand() % (max - min + 1);

    return randomValue;
}

void func(int &a)
{
    a = 20;
}
void gotoXY(int x, int y) {
    
    COORD c;
    HANDLE H = GetStdHandle(STD_OUTPUT_HANDLE);
    c.X = x;
    c.Y = y;
    SetConsoleCursorPosition(H,c);
}
int main()
{
    // while (true)
    // {
    //     int i;
    //     cin >> i;

    //     if (i % 6 == 0)
    //     {
    //         cout << "yeee" << endl;
    //     }
    //     else
    //     {
    //         cout << i << endl;
    //     }
    // }

    // vector<int> vec = {1,2,3,4,5,6};
    // int p = Find(vec,6);
    // cout<<p<<endl;

    // for (int i = 0;i<=10;i++){
    //     int r = getRandomInt(10,20);
    //     cout<<r<<endl;

    // }
    // initscr();
    // move(10, 10);
    // printf("Hello, world!")

    // refresh();
    // getch();

    // endwin();

    // int a = 10;
    // printf("before: %d\n", a);
    // func(a);
    // printf("after: %d\n", a);
    // int a = 10;
    // int *p = &a;
    // cout<<p<<endl;
    // cout<<*p<<endl;
    // // cout<<a<<endl;
    // // Screen screen; // 创建一个 Screen 对象
    // // screen.Clear(); // 清除画布

    // // // 画一个长方形
    // // screen.DrawLine(10, 10, 50, 10, 255); // 从 (10, 10) 到 (50, 10) 绘制横线
    // // screen.DrawLine(10, 10, 10, 30, 255); // 从 (10, 10) 到 (10, 30) 绘制竖线
    // // screen.DrawLine(50, 10, 50, 30, 255); // 从 (50, 10) 到 (50, 30) 绘制竖线
    // // screen.DrawLine(10, 30, 50, 30, 255); // 从 (10, 30) 到 (50, 30) 绘制横线

    // // screen.Show(); // 将画布渲染至屏幕
    // string str = "";
    // for (int i = 0; i < 100 * 100; i++)
    // {
    //     if (i == 10)
    //     {
    //         str[i] = '\n';
    //     }
    //     str[i] = '@';
    // }
    // fputs(str, stdout);

    //画30度的线
    // 创建一个Screen对象
    Screen screen;

    // 画一个长度为10的线段，初始坐标为(1, 20)
    // 计算线段的终点坐标
    int length = 30;
    double angle = 70;  // 角度
    int x1 = 10;
    int y1 = 20;
    int x2 = x1 + length * cos(angle * M_PI / 180); // 计算结束点的x坐标
    int y2 = y1 + length * sin(angle * M_PI / 180); // 计算结束点的y坐标

    // 画线
    screen.DrawLine(x1, y1, x2, y2, 100);  // 在画布上画一条指定起点和长度的线段，亮度为255

    // 将画布渲染至屏幕
    screen.Show();





    getchar();
    getchar();
}