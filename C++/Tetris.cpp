#include <iostream>
#include <stdio.h>
#include <vector>



std::vector<std::vector<int>> initTetris(){
    std::vector<std::vector<int>> tetrisData;
    for (int i = 0; i < 40; i++) {
        for (int j = 0; j < 10; j++) {
            tetrisData.push_back(std::vector<int>(10, 0));
        }

    }
    return tetrisData;
}


int main()
{
    initTetris();
    getchar();
    return 0;
}


/**



*/