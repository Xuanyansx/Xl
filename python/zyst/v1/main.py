import tkinter as tk
import simplejson as json
import random as ra
from tkinter import messagebox as mBox

gui = tk.Tk()
gui.geometry("700x700")
gui.resizable(False, False)
gui.title("职业技能v1版")


with open("data/stats.json", mode="r", encoding="UTF-8") as f:
    stats = json.load(f)

with open("data/qStatus.json",mode="r",encoding="UTF-8") as f:
    List = json.load(f)["status"]
vars = [tk.IntVar() for _ in range(len(List))]

lastOpt = 0
isPress = 1
opt = 0
zqls = {} #正确率
"""
{
    groupId:对的题目数量
}

"""

qSum = 0
Num = 0

groups = []
D = {}#本轮出现的题目id

FF = tk.Frame(gui, width=700, height=500, bg='light grey')
FF.pack()
"""
{
    groupId:[id1,id2,id3],
    groupId1:[id1,id2,id3],
    ...
}

"""

def handleQuestion(group, ID,MOD,q = None) -> object:  # 返回一个题目（object形式）
    print("=+="*10)
    with open(f'data/{group}.json', mode='r+', encoding='UTF-8') as question:
        data = json.load(question)
    if MOD == "g":
        res = data[str(ID)]
    else :
        data[str(ID)] = q
        with open(f"data/{group}.json",mode='w',encoding="UTF-8") as f:
            json.dump(data,f)
        res = True
    return res

def optionEvent(*res):
    global lastOpt
    global isPress
    global opt
    if res[0] == "b":
        opt = res[2]
        res[3][lastOpt].config(bg='white')
        res[3][res[2]].config(bg='blue')
        lastOpt = res[2]
        if isPress:
            res[1].pack()
    if res[0] == "s":
        submiBt(opt,res[1],res[2])
    isPress = 0

def submiBt(opt,Q,M):
    global zqls
    F = tk.Frame(M,width=400)
    txt = tk.Label(F,text=f"答案： {Q['answer']}")
    txt1 = tk.Label(F,text=f"{Q['explanation']}",width=400,wraplength=600)
    bt = tk.Button(F,width=20,height=20)
    answers = {
        "A":0,
        "B":1,
        "C":2,
        "D":3
    }
    
    txt.pack(pady=5)
    txt1.pack(pady=5)
    bt.pack()
    F.pack()
    if opt == answers[Q["answer"]]:
        zqls[Q["group"]]+=1
        print(zqls)
        bt.config(bg='green',text="正确,前往下一题",command=lambda : chuti(M))
    else :
        bt.config(bg='red',text="错误,前往下一题",command=lambda : chuti(M))

    


def mainfm(M, Q,qNum):
    t = Q["question"]
    item = Q["options"]
    F = tk.Frame(M,width=700,height=500)
    T = tk.Label(F, text=t, width=500, highlightbackground='red', highlightthickness=3, wraplength=500)
    txt = tk.Label(F,text= f"题目进度: {qNum}/{qSum}",bg='yellow')
    T.pack(ipady=5, ipadx=5)
    txt.pack(anchor='nw')
    bts = []
    opt = ["A", "B", "C", "D"]

    sbt = tk.Button(F, text="提交", command=lambda: optionEvent("s",Q,F,qNum))
    for i in range(len(item)):
        if item[i][0] == '':
            break
        bt = tk.Button(F, text=f"选项{opt[i]}  {item[i][0]}", command=lambda i=i: optionEvent("b", sbt, i, bts),wraplength=300)
        bt.pack()
        bts.append(bt)
    F.pack()


# 选择题目范围 【点击选择（用选择按钮）  输入选择 既是输入组id
# 显示已经做题组的准确率

def fanye(F, ID, TYPE):
    F.destroy()
    if TYPE:
        if ID[0] == 0:
            qGroup(FF, List[ID[0]:ID[1] + 1])
            print(List[ID[0]:ID[1] + 1])
            return
        qGroup(FF, List[ID[0] - 10:ID[0]])
    else:
        if ID[1] == len(List) - 1:
            print(ID[0])
            print(ID[1])
            qGroup(FF, List[ID[0]:ID[1] + 1])
            return
        qGroup(FF, List[ID[1] + 1:ID[1] + 11])
        print(List[ID[1] + 1:ID[1] + 11])
    pass


def qGroup(M, idList):  # 题目组
    s = 1

    Fm = tk.Frame(M, width=200, height=500, highlightbackground='red', highlightthickness=3)
    for i in idList:
        if s:
            HID = i[0]
            s = 0
        print(i[0])
        var = vars[i[0]]
        cb = tk.Checkbutton(Fm,text=f"第{i[0] + 1}组题目  {'未做' if i[1] == None else f'正确率{i[1]}'}", bg='green', variable=var)
        cb.pack(pady=5)
        EID = i[0]

    bt1 = tk.Button(Fm, text="上一页", width=155, bg='red', command=lambda: fanye(Fm, [HID, EID], 1))
    bt2 = tk.Button(Fm, text="下一页", width=155, bg='red', command=lambda: fanye(Fm, [HID, EID], 0))
    bt2.pack(side='bottom')
    bt1.pack(side='bottom')
    Fm.place(relx=1, rely=0, anchor='ne')
    Fm.pack_propagate(0)


def displayGroup(txt):
    t = ""
    for i, var in enumerate(vars):
        if var.get():
            t = t + f"第{i + 1}号题组 "
    

    txt.config(text=f"{t} ", fg='blue')

def chuti(F):
    global isPress
    global Num
    global D
    global FF
    global qSum
    isPress = 1
    if Num == qSum:
        if mBox.askyesno("询问","您的题目以全部完成，是否重新选择？(否既是退出程序)"):
            for i in groups:
                vars[i].set(0)
            FF = tk.Frame(gui, width=700, height=500, bg='light grey')
            qGroup(FF,List[0:10])
            selectionQ(FF)
            F.destroy()
            FF.pack()
            Num = 0
            qSum = 0
            return
        else :
            for i in groups:
                if i == stats["groupNum"]:
                    zql = (zqls[i]/(stats["lastG"]+1))*100
                else :
                    zql = (zqls[i]/50)*100
                List[i] = [i,int(zql)]
                print(zql)
            with open("data/qStatus.json",mode="w",encoding="UTF-8") as f:
                json.dump({"status":List},f)
            exit()
                
    while True:
        group = ra.randint(0, len(groups) - 1)
        if groups[group] == stats["groupNum"]:
            ID = ra.randint(0,stats["lastG"])
        else :
            ID = ra.randint(0,49)
        print(D[groups[group]])
        if  D[groups[group]] != []: 
            if ID in D[groups[group]]:
                continue
        break
    D[groups[group]].append(ID)
    Q = handleQuestion(groups[group], ID,MOD="g")
    
    Q["occurrences"] +=1
    Num +=1
    handleQuestion(groups[group],ID,MOD="h",q=Q)
        
    F.destroy()
    print(Q)
    mainfm(gui,Q,Num)
    pass

    

def start(F):
    global qSum
    global groups
    qNum = 0 #题目总共数量
    
    for i, var in enumerate(vars):
        if var.get():
            groups.append(i)
            D[i] = []#初始化
            zqls[i] = 0
            if i == stats["groupNum"]:
                qNum = qNum +(stats["lastG"]+1)
                #因为是采用从0开始的计数方式，为了方便使用这里加1
            else :
                qNum = qNum + 50
    qSum = qNum
    if groups == []:
        return
    chuti(F)

    
    
def selectionQ(M):
    Fm = tk.Frame(M, width=400, height=500, bg='light grey')
    txt = tk.Label(Fm,text=f"在右侧选择题组（1组50题），选择完点击开始，程序会随机从选择的题组里面出题\n\n已选择题组", wraplength=400,font=("Helvetica", 12), bg='light grey', justify='left')
    txt1 = tk.Label(Fm, wraplength=400, font=("Helvetica", 12), bg='light grey', justify='left')
    txt.pack(side='top', pady=10)
    txt1.pack()
    
    bt0 = tk.Button(Fm, text="显示选择的题组", command=lambda: displayGroup(txt1), bg='blue')
    bt = tk.Button(Fm, text="开始", bg='blue', command=lambda :start(FF))
    bt.pack(side='bottom')
    bt0.pack(side='bottom')
    Fm.place(anchor='nw')
    Fm.pack_propagate(0)

def on_closing():
    
    pass





qGroup(FF,List[0:10])
selectionQ(FF)

gui.protocol("WM_DELETE_WINDOW", on_closing)

gui.mainloop()



"""
假设要从10组题目里面随机出题，全部打开一遍显然不行
我想的是   打开文件->读取题目->关闭文件
在出题过程看上去确实繁琐，但这也是我想出的唯一一个优化的办法了


12/28要开始写‘开始’按钮了，第一次写这种程序思路还是不怎么清晰..




"""
