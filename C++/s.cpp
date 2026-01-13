#include <windows.h>
#include <iostream>
#include <stdio.h>

// 锁定鼠标和键盘的函数
void lock_input(int m) {
    int seconds = m*60;
    BlockInput(TRUE);
    for (int i = seconds;i>=0;i--){
        printf("\r倒计时%2d",i);
        Sleep(1000);
    };
    BlockInput(FALSE);
    return;
}

int main() {
    int m;
    char yorn;
    while (true)
    {
        printf("请输入锁定的分钟: ");
        std::cin >> m;
        lock_input(m);
        printf("\r成功解锁！本次锁定%d分钟，是否再来一轮锁定？(y / n)",m);
        std::cin >> yorn;
        if (yorn=='y' || yorn =='Y'){
            continue;
        }
        else{
            break;
        }
    }

    return 0;
}
