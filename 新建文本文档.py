import random
import tkinter as tk

# 创建窗口
window = tk.Tk()
window.title("石头剪子布游戏")
window.geometry("300x150")

# 定义游戏逻辑
def play_game(user_choice):
    choices = ["石头", "剪子", "布"]
    computer_choice = random.choice(choices)
    result = ""
    if user_choice == computer_choice:
        result = "平局"
    elif user_choice == "石头" and computer_choice == "剪子" \
        or user_choice == "剪子" and computer_choice == "布" \
        or user_choice == "布" and computer_choice == "石头":
        result = "你赢了！"
    else:
        result = "电脑赢了！"
    result_label.config(text="你出的是" + user_choice + "，电脑出的是" + computer_choice + "，" + result)

# 创建控件
choice_label = tk.Label(window, text="请选择：")
choice_label.pack()

rock_button = tk.Button(window, text="石头", command=lambda: play_game("石头"))
rock_button.pack(side=tk.LEFT, padx=5)

scissors_button = tk.Button(window, text="剪子", command=lambda: play_game("剪子"))
scissors_button.pack(side=tk.LEFT, padx=5)

paper_button = tk.Button(window, text="布", command=lambda: play_game("布"))
paper_button.pack(side=tk.LEFT, padx=5)

result_label = tk.Label(window, text="")
result_label.pack()

# 进入主循环
window.mainloop()
