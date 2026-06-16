#include <easyx.h>
#include <stdio.h>
#include <Windows.h>


int main() {
	initgraph(810, 800);
	HWND hConsole = GetConsoleWindow();
	SetWindowPos(hConsole, HWND_TOP, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_SHOWWINDOW);
	int posX[] = { 0,10};
	int posY[] = { 0,10};

	int pos[] = { 0,100 };
	
	int x;
	int y;
	ExMessage msg;
	while (true)
	{
		cleardevice();
		rectangle(posX[0], posY[0], posX[1], posY[1]);
		if (peekmessage(&msg, EX_MOUSE)) {
			x = msg.x/pos[1];
			y = msg.y/pos[1];
			for (int i = 0; i <= 1; i++) {
				posX[i] = pos[i] + x * pos[1];
				posY[i] = pos[i] + y * pos[1];
			}

			printf("\n%d,%d", x, y);

	}


		
		
	}

}