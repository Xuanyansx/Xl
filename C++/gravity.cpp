#include <stdio.h>
#include <iostream>

char *input(const char *str)
{
    char *res = (char *)malloc(64 * sizeof(char));
    printf("%s", str);
    scanf("%63s", res); // 限制输入长度
    return res;
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

void display2D(int **arr,int w,int h){
    // 墙-1 球1 空气0
    int pos;
    w--;
    h--;
    string game;
    for(int i=0;i<=w;i++){
        for(int j = 0;j<=h;j++){
            pos = arr[i][j];
            game = game + (pos == -1 ? "■" : pos == 0 ? "  ": pos == 1   ? "■": "□");
        }
        game = game+"\n";

    }

    cout << game <<endl;

}

int ballMove(){}

int main(){
    int w = 45;
    int h = 85;

    int F = 0;
    /*
    基本力的方向(重力)
    -1 0 1 2
    上1 下0
    左1 右2
    */
    int f = 125
    /*
    力的方向
    
    */


    int **Map = init2D(w,h);//初始化地图
    Map[84][27] = 1;//球初始的位置
    

}

/*
模拟一个球的运动






*/