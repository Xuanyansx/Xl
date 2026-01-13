from pynput import mouse, keyboard
import time
import threading

# 设置两个全局变量来控制点击状态和记录点击次数
clicking = False
click_count = 0
click_interval = 0.1  # 默认点击间隔为0.1秒

# 定义一个函数来模拟鼠标点击
def click_mouse():
    global clicking
    global click_count
    global click_interval
    with mouse.Controller() as controller:
        while True:
            if clicking:
                controller.click(mouse.Button.left, 1)
                click_count += 1
                print(f"已点击{click_count}次")
                time.sleep(click_interval)
            else:
                time.sleep(0.1)

# 创建并启动一个线程来运行鼠标点击函数
t = threading.Thread(target=click_mouse)
t.start()

# 定义一个函数来处理键盘按键事件
def on_press(key):
    global clicking
    global click_interval
    global t

    # 如果按下的是右Ctrl键，就改变点击状态
    if key == keyboard.Key.ctrl_r:
        clicking = not clicking
        if clicking:
            print("开始点击")
        else:
            print("停止点击")

    if key == keyboard.Key.shift_r and not clicking:
        set_interval = input("请输入点击速度（秒）：")
        try:
            click_interval = float(set_interval)
            print(f"点击速度已设置为{click_interval}秒")
        except ValueError:
            print("无效的输入，请输入一个有效的数字。")

# 使用键盘监听器来监听按键事件
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
