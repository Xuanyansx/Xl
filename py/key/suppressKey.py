import threading
from pynput import mouse, keyboard
import tkinter as tk
import time

list2 = []
b = False
bb = True

def on_press(key):
    print(key)
    list = ['w', 'w', 'e', '1', '1', '4', '5']
    global list2
    global b
    global bb
    if str(key) == "Key.esc":
        b = True
        list2 = []
        return
    if b:
        print(list2)
        list2.append(str(key).replace("'", ""))
        if len(list2) == len(list):
            if list2 == list:
                bb = False
            else:
                list2 = []
                b = False

def mouse_mover():
    # 创建一个鼠标控制器
    mouse_controller = mouse.Controller()

    # 获取屏幕的宽度
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()

    # 将鼠标移动到屏幕的右上角
    mouse_controller.position = (0,screen_width)

# 创建一个键盘监听器
keyboard_listener = keyboard.Listener(on_press=on_press,suppress=True)
keyboard_listener.start()

# 创建一个线程来移动鼠标

mouse_thread = threading.Thread(target=mouse_mover)
mouse_thread.start()
