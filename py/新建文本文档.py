import ctypes
import time

# 锁定鼠标和键盘的函数
def lock_input():
    # 锁定鼠标
    ctypes.windll.user32.BlockInput(True)
    # 锁定10秒，你可以修改这个时间
    time.sleep(10)
    # 解锁鼠标和键盘
    ctypes.windll.user32.BlockInput(False)

lock_input()
