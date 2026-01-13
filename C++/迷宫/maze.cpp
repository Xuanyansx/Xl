#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <iostream>
#include <time.h>
#include <windows.h>


using namespace std;

char *input(char *str)
{
    char *res = (char *)malloc(64 * sizeof(char));
    printf("%s", str);
    scanf("%63s", res); // 限制输入长度
    return res;
}

void hideCursor(SHORT x, SHORT y)
{
    COORD pos = {x, y};
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE); // 获取标准输出设备句柄
    SetConsoleCursorPosition(hOut, pos);           // 两个参数分别是指定哪个窗体，具体位置

    HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_CURSOR_INFO CursorInfo;
    GetConsoleCursorInfo(handle, &CursorInfo); // 获取控制台光标信息
    CursorInfo.bVisible = false;               // 隐藏控制台光标
    SetConsoleCursorInfo(handle, &CursorInfo); // 设置控制台光标状态
}

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

// -1 为墙  0 为空气  1 为角色

int Find(vector<int> vec,int key){
    int res = -1;

    for (int i = 0;i<vec.size();i++){
        if (vec[i] == key){
            res = i;
            break;
        }
        
    }

    return res;

}
struct Maze
{
    vector<int> mazeData;
    vector<int> nodes;
    int point;
};

vector<int> initMaze(int size)
{

    vector<int> arr(size * size);
    for (int i = 0; i <= size * size; i++)
    {
        arr[i] = -1;
    }
    return arr;
}



Maze generateMaze(Maze &data,int size,int point)
{
    int mapSize = size * 2 + 1;
    int flag;
    int nextCoord;
    int direction[4] = {-(mapSize*2),mapSize*2,-2,2};
    int direction1[4] = {-mapSize,mapSize,-1,1};
    data.mazeData[point] = 0;
    if (Find(data.nodes,point)==-1){
        data.nodes.push_back(point);
    }


Re:
    flag = getRandomInt(0,3);
    if (data.nodes.size()==size*size){
        data.point = nextCoord;
        data.mazeData[point+direction1[flag]] = 0;
        cout<<"kkkkkkkkkkkkkkk"<<endl;
        cout<<data.nodes.size()<<endl;
        cout<<data.nodes.back()<<endl;
        cout<<data.nodes[Find(data.nodes,data.nodes.back())-1]<<endl;
        cout<<"kkkkkkkkkkkkkkk"<<endl;
        return data;
    }

    nextCoord = point+direction[flag];
    // printf("\rnext:%3d point:%2d\n",nextCoord,point);

    if ((nextCoord < mapSize) || (nextCoord % mapSize == 0) || 
    ((nextCoord - (mapSize - 1)) % mapSize == 0) || (nextCoord > mapSize * mapSize - mapSize)||
    (nextCoord>=mapSize*mapSize)||(nextCoord<0)||
    (Find(data.nodes,nextCoord)!=-1))
    {
        // printf("\r              index:  %3d   point:%3d   size:%3d",nextCoord,point,data.nodes.size());
        if (data.nodes[0]==point){
            point = data.nodes.back();
            goto Re;
        }
        point = data.nodes[Find(data.nodes,point)-1];
        goto Re;
    }
    data.point = nextCoord;
    data.mazeData[point+direction1[flag]] = 0;
    // printf("\r\n%3d   %3d\n",Find(data.nodes,point),point);
    // cout<<data.nodes.size()<<endl;
    return data;
}

void displayMaze(vector<int> arr, int mapSize)
{
    for (int i = 0; i < mapSize * mapSize; i++)
    {
        if (arr[i] == -1)
        {
            printf("■");
        }
        else if(arr[i]==0)
        {
            printf("  ");
            
        }
        else
        {
            printf("■");
        }
        // printf("%5d",i);
        if ((i - (mapSize - 1)) % mapSize == 0)
        {
            printf("\n");
        }
    }
}

int main()
{
    int mSize = 40;
    int mapSize = mSize * 2 + 1;
    int point = mapSize +1;//起点
    int r;
    int maxSize = mSize*mSize;

    Maze data,res;
    int *arr = new int[mapSize*mapSize];

    data.mazeData = initMaze(mapSize);
    
    while(true){
        // Sleep(100);
        generateMaze(data,mSize,point);
            // printf("%d",res.nodes.size());


        // cout<<1<<endl;

        hideCursor(0,0);
        displayMaze(data.mazeData, mapSize);
        point = data.point;
        cout<<"vvvvvvvvvvvvv"<<endl;
        cout<<data.nodes.size()<<endl;
        cout<<data.nodes.back()<<endl;
        cout<<"vvvvvvvvvvvvv"<<endl;
        // if (data.nodes.size() == Size*Size){
        //     break;
        //     cout<<"\n迷宫生成完毕"<<endl;
        // }
        // printf("Bool:%d\n",data.nodes.size() == maxSize);
        if (data.nodes.size() == maxSize){
            printf("\n迷宫生成完毕");
            break;
        }
    }
    getchar();
    /*
    示例:3*3的地图

    [
    00,01,02,03,04,05,06,
    07,08,09,10,11,12,13,
    14,15,16,17,18,19,20,
    21,22,23,24,25,26,27,
    28,29,30,31,32,33,34,
    35,36,37,38,39,40,41,
    42,43,44,45,46,47,48
    ]


    横向移动2 pos +/- 2
    纵向移动 pos +/- mapSize*2

    */

    return 0;
}
