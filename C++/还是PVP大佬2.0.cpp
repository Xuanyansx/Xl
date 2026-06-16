#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <windows.h>

#define width 40
#define height 15
#define zombieSpeed 2 //Խ��Խ��

int main() {
    int x = 24;
    int y = 1;
    int pvpFlag = 0;
    int zombieFlag = 0;
	char gameBoard[15][40] = {"                                       ","                                       ","+-+-+-+-+-+-+-+-+-+-+                  ","|                   |                  ","+                   +                  ","|                   |                  ","+                   +-                 ","|                   *                  ","+                   +-                 ","|                   |                  ","+                   +                  ","|                   |                  ","+-+-+-+-+-+-+-+-+-+-+                  ","                                       " ,"                                       " };

	while (1) {
        /*��ӡ����*/
        char buffer[height * width + height];
        buffer[0] = '\0';
        for (int i = 0; i < height; ++i) {
            for (int j = 0; j < width; ++j) {
                sprintf_s(buffer, "%s%c", buffer, gameBoard[i][j]);
            }
            sprintf_s(buffer, "%s\n", buffer);
        }
        system("cls");
        printf("%s", buffer);

        /*/*��ʬ�ƶ�
        for (int i = 0; i < width-1; i++) {
            if (gameBoard[7][i] == 'Z') {
                gameBoard[7][i] = ' ';
                gameBoard[7][i+1] = 'Z';
                i++;
            }
        }
        */
        /*����ƶ�*/
        gameBoard[y][x] = ' ';
        if (_kbhit()) {
            switch (_getch()) {
            case 'w':
                --y;
                if (gameBoard[y][x] == '+' || gameBoard[y][x] == '-' || gameBoard[y][x] == '|') ++y;
                break;
            case 's':
                ++y;
                if (gameBoard[y][x] == '+' || gameBoard[y][x] == '-' || gameBoard[y][x] == '|') --y;
                break;
            case 'a':
                --x;
                if (gameBoard[y][x] == '+' || gameBoard[y][x] == '-' || gameBoard[y][x] == '|') ++x;
                break;
            case 'd':
                ++x;
                if (gameBoard[y][x] == '+' || gameBoard[y][x] == '-' || gameBoard[y][x] == '|') --x;
                break;
            default:
                continue;
            }
        }
        gameBoard[y][x] = 'P';
        int pP;
        if (y > 1 && y < 12 && x > 0 && x < 20) {
            pP = 0;
        }
        else if (gameBoard[7][20] == 'P') {
            pP = 3;
        }
        else pP = 1;

        /*��ʬѰ·*/
        int flagXY = 0;
        int flagX[100];
        int flagY[100];
        zombieFlag++;
        if (zombieFlag > zombieSpeed) {
            zombieFlag = 0;
        }
        for (int i = 0; i < height; ++i) {
            for (int j = 0; j < width; ++j) {
                int flag = 1;
                for (int k = 0; k < flagXY; ++k) {
                    if (flagX[k] == j && flagY[k] == i) {
                        flag = 0;
                    }
                }
                if (gameBoard[i][j] == 'Z' && flag && !zombieFlag) {
                    int zX = j;
                    int zY = i;
                    gameBoard[i][j] = ' ';
                    int zP;
                    if (zY > 1 && zY < 12 && zX > 0 && zX < 20) {
                        zP = 0;
                    }
                    else if (zY == 7 && zX == 20) {
                        zP = 3;
                    }
                    else zP = 1;

                    if (pP == 3 || zP == pP) {
                        if (zX > x) {
                            zX = zX - 1;
                        }
                        else if (zX == x) {
                            zX = zX;
                        }
                        else {
                            zX = zX + 1;
                        }
                        if (zY > y) {
                            zY = zY - 1;
                        }
                        else if (zY == y) {
                            zY = zY;
                        }
                        else {
                            zY = zY + 1;
                        }
                    }
                    else if (zP == 3) {
                        if (zX > x) {
                            zX = zX - 1;
                        }
                        else zX = zX + 1;
                    }
                    else {
                        if (zX > 20) {
                            zX = zX - 1;
                        }
                        else if (zX == 20) {
                            zX = zX;
                        }
                        else {
                            zX = zX + 1;
                        }
                        if (zY > 7) {
                            zY = zY - 1;
                        }
                        else if (zY == 7) {
                            zY = zY;
                        }
                        else {
                            zY = zY + 1;
                        }
                    }
                    gameBoard[zY][zX] = 'Z';
                    flagX[flagXY] = zX;
                    flagY[flagXY] = zY;
                    flagXY++;
                }
                
            }
        }
        

        /*ѹ����*/
        if (pvpFlag > 10) {
            pvpFlag = 0;
        }
        if (pvpFlag) {
            printf("     ����PVP����");
            pvpFlag++;
        }
        if (gameBoard[7][20] == 'P' || gameBoard[7][20] == 'Z') {
            gameBoard[7][5] = 'Z';
            pvpFlag++;
        }
        else {
            gameBoard[7][20] = '*';
        }

        /*��Ϸ�ٶ�*/
		Sleep(200);
	}
}