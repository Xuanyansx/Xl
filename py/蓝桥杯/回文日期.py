








"""dd
20 20 
02 02

20 21 
12 02

21 21 
12 12

"""
n = input()
yyyy = n[:4]
flag = True

def check_date(date):
    m = ['pass',31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    yyyy = int(date[:4])
    mm = int(date[4:6])
    dd = int(date[6:])
    if (yyyy % 400 == 0) or (yyyy % 4 == 0 and yyyy % 100 != 0):
        if mm==2 and dd<=29:
            return True
    return 1<=mm<=12 and 1<=dd<=m[mm]

while True:
    mmdd = yyyy[::-1]
    if check_date(yyyy+mmdd) and flag:
        print(yyyy+mmdd)
        flag = False
        continue
    if yyyy[:2] == yyyy[2:] and check_date(yyyy+mmdd):
        print(yyyy+mmdd)
        break
    yyyy = f'{int(yyyy)+1}'
    
