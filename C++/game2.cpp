#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include <ctime>
using namespace std;


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


void display2D(int **arr,int w,int h){
    // 墙-1 球2 拍子1
    int pos;
    w--;
    h--;
    string game;
    for(int i=0;i<=w;i++){
        for(int j = 0;j<=h;j++){
            pos = arr[i][j];
            game = game + (pos == -1 ? "■" : pos == 0 ? "  ": pos == 1   ? "■": "□");
            if (j==h){
                game = game+"\n";
            }
        }
    }

    cout << game <<endl;

}



int **init2D(int w,int h){
    
    w --;
    h --;
    int **arr = (int **)malloc(w * sizeof(int*));
    for (int i = 0;i<=w;i++){
        arr[i] = (int *)malloc(h *sizeof(int));
        for(int j = 0;j<=h;j++){
            if(i==0||i==w||j==0||j==h){
                arr[i][j]=-1;
            }
            else{
                arr[i][j] = 0;
            }
        }
    }

    // P1Pos 
    // p2Pos

    // bowPos
    return arr;
}


int main(){
    int w = 45;//高 byd当时脑抽风了，高度h和宽w写反了..  现在好了，也不会改了-------
    int h = 85;//宽 


    int **arr = init2D(w,h);
    display2D(arr,w,h);


    getchar();
    return 0;
    
}


/*
(0,0)  (0,1)  (0,2)  (0,3)  (0,4)
(1,0)  (1,1)  (1,2)  (1,3)  (1,4)
(2,0)  (2,1)  (2,2)  (2,3)  (2,4)
(3,0)  (3,1)  (3,2)  (3,3)  (3,4)
(4,0)  (4,1)  (4,2)  (4,3)  (4,4)
(5,0)  (5,1)  (5,2)  (5,3)  (5,4)
(6,0)  (6,1)  (6,2)  (6,3)  (6,4)
(7,0)  (7,1)  (7,2)  (7,3)  (7,4)
(8,0)  (8,1)  (8,2)  (8,3)  (8,4)
(9,0)  (9,1)  (9,2)  (9,3)  (9,4)




    球的坐标由玩家决定
    开局先决定哪位玩家发球

    中间要有有面墙 这个墙并不是完全封闭的，它的7/6是它的缺口












*/