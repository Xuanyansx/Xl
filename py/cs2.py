# import tkinter as tk


# gui = tk.Tk()
# gui.geometry("500x500")

# def fanye(List)
#     pass

# def init(M,idList):
#     Fm = tk.Frame(M,width=200,height=600,highlightbackground='red',highlightthickness=3)
#     for i in idList:
#         cb = tk.Checkbutton(Fm,text=f"第{i[0]+1}组题目  {'未做' if i[1]==None else f'正确率{i[1]}'}",bg='blue')        
#         cb.pack(pady=5)

#     bt1 = tk.Button(Fm,text="上一页",width=155,bg='red',command=lambda : fanye(idList))
#     bt2 = tk.Button(Fm,text="下一页",width=155,bg='red')
#     bt1.pack()
#     bt2.pack()
#     Fm.place(relx=1, rely=0, anchor='ne')
    
    # Fm.pack_propagate(0)

# def Func(List):
#     pass

# cbList = []

# for i in range(5):
#     cb = tk.Checkbutton(gui,text=f"{i}",command=lambda : Func(cbList))



# gui.mainloop()
# import random as re
# arr = [0]*500
# for i in range(15):
#     arr[re.randint(0,500)] = 1



# print(1 in arr)


import tkinter as tk
from tkinter import messagebox

def on_closing():
    if messagebox.askokcancel("退出", "你确定要退出吗？"):
        root.destroy()

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()


