





n,A,B,C = input().split()

def move(n,f,m,t):
    
    
    if n==0:
        return
    
    move(n-1,f,t,m)
    #2 A C B   1 A B C     A=>C
    print(f"{n} {f}=>{t}")
    move(n-1,m,f,t)
    # B A C    B C A B=>C


move(int(n),A,B,C)