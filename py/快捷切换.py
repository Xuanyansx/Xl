import keyboard as k


arr = ["1","2"]
i = 0
j = 1

def Func():
    global i
    i +=1
    if i > 1:
        i = 0
    k.press_and_release(arr[i])

def Func2(key):
    global arr
    global i


    if key.name == "q":
        Func()
    elif key.name.isdigit() and key.name not in arr and key.name != "0":
        if i == 0:
            i = 1
        else :
            i = 0
        arr[i] = key.name
        
    pass

k.on_press(Func2)

k.wait()
