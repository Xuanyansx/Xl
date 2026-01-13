#include<stdio.h>
#include <unistd.h>

int main(){

    // int arr[5][4] = [[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14],[15,16,17,18,19]];
    for (int i = 0;i<=5;i++){
        sleep(1);
        
        for (int j = 0;j<=4;j++){
            printf("%d",j);
        }
        printf("\n");
    }

    return 0;
}