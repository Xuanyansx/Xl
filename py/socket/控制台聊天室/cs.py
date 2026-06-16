# from prompt_toolkit.completion import WordCompleter
# from prompt_toolkit import prompt


# names = ["张三", "李四", "王五", "赵六", "钱七"]

# cmd = ["aaaa","bbbb","cccc"]

# name = [f"@{i}" for i in names]


# command_completer = WordCompleter(name+cmd, ignore_case=True)

# while True:
#     print()
#     cmd = prompt(completer=command_completer)

#     print(cmd)

# import time

# def a():
#     for i in range(20):
#         print(i)
#         time.sleep(0.3)
#         yield

# def c():
#     f = a()
#     for i in range(0,40,2):
#         print(i)
#         next(a())

#         time.sleep(0.1)

# def b():
#     af = a()
#     for i in range(0,100,2):
#         print(">",i)
#         next(af)



# t = time.time()
# c()
# # a()
# print(time.time()-t)

# a = b'41'
# print(len(a))


# b = '带汉化'.encode('utf-8')
# bl = len(b)
# bt = bytes(str(bl),'utf-8').zfill(4)
# print(bt,bl)






# def test(e):
#     print(e)
#     while True:
#         y = yield
#         print("dw ",y)

# def a():
#     print(1111111)
#     while True:
#         c = input(">>>>")
#         yield c

# def c():
#     tf = test(123) 
#     af = a()
#     next(tf)
#     while True:
#         data = next(af)
#         tf.send(data)


# c()

# while True:
#     i = 0
#     i+=1
#     if i>=10:
#         break
# else:
#     print(111)
# import json
# a = '{"a":"1", "b":"1"}'
# c=json.loads(a)
# print(c, type(c))

# from sympy import cofactors


# a = 20
# while a>=20:
#     if True:
#         print(a)
#         continue



# a = 1

# b = a

# print(id(a))
# print(id(b))

# b+=1
# print(b)
# print(a)

# print(id(a))
# print(id(b))



# a = "dwdw"
# b = a

# print(a)
# print(b)

# a = "wqdqdwqdwqdw"

# print(a)
# print(b)


# class test:
#     def __init__(self,name):
#         self.name = name
    
#     def p(self,msg):
#         res = self.name+msg
#         return res
    

# a = test("eeee")
# print(a.p("dwdwd"))


# a = [(1,2),(4,5),(7,9),(5,6)]
# for b,c in a:
#     print(b,c)


# a = {1:2,3:4,5:6}

# for i,j in a.items():
#     if i == 3:
#         print(i,j)

# class aaa:
#     pass


# a = aaa()
# a.name = 1
# print(a.name)

# from ast import mod
# from threading import Thread
# import time



# def ff():
#         while True:
#             tt = f.readline()
#             print(tt)
#             if tt == "":
#                 break

# def read(f):
#     while True:
#         txt = f.readline()
#         print(txt)
#         if txt == "":
#             break

# if __name__ == "__main__":
#     ti = time.time()
#     li = []
#     with open("C:\deleted_files.txt",mode="r",encoding='utf-16') as f:
#         for i in range(10):
#             tt = Thread(target=read,args=(f,))
#             tt.start()
#             li.append(tt)
#         for i in li:
#             i.join()
#         # read(f)
#     print(time.time() - ti)


# tt = time.time()
# a()
# b()
# print(time.time() - tt)


# while True:
#     a = input(">")
#     if a[0] in ['1','0']:
#         print("true")
#         continue
#     print("111")

# import threading
# class a(threading.Thread):
    
#     @classmethod
#     def a(cls):
#           cls.ru1n(11)
    
#     @staticmethod
#     def ru1n(a):
#             print(a)

# a.a()


# def b():
#     while True:
#         data = yield
#         print(data)

# def a():
#     fb = b()
#     next(fb)
#     for i in range(10):
#         fb.send(i)

# a()

# def aa():
#     for i in range(10):
#         yield i
#     yield 'e'

# def c():
#     fb = b()
#     faa = aa()
#     next(fb)
#     while True:
#         data = next(faa)
#         if data == 'e':
#             break
#         fb.send(data)

# c().


# class a():
#     def __init__(self):
#         self.name = '111'

# class b():
#     def __init__(self,aa:a):
#         self.aa = aa
#         self.name = aa.name
    
#     def ff(self):
#         print(self.name)
#     def __dwdwd__():
#         pass
# d = a()

# c = b(d)
# c.ff()

# d.name='dwdwd'
# c.ff()

class a():
    def __init__(self,name,age):
        self.name = name
        self.age = age
        self.ww = ''

def d(ad:a):
    ad.name = 'oo'
    ad.ww = '123'

def c(ac:a):
    print(ac.age)
    print(ac.ww)
    print(ac.name)
    d(ac)

def b():
    aa = a('qwe',22)
    c(a)










        