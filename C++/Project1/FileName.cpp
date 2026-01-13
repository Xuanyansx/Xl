#include <graphics.h>

#include <iostream>
#include <time.h>

int main() {
	int posX = 10;
	int posY = 10;
	ExMessage msg;
	
	printf("%ws", GetEasyXVer());
	initgraph(1000, 1000);
	circle(posX, posY, 10);
	
	while (true) {

		while (peekmessage(&msg))
		{
			if (msg.message == WM_MOUSEMOVE) {
				putpixel(posX, posY, RGB(222,333,444));
				msg = getmessage(EX_MOUSE);
				posX = msg.x;
				posY = msg.y;
				
			}
			Sleep(1);

		}

		Sleep(1);


	};
	return 0;

};