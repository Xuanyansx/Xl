a = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]

dxdy = [(0,-1),(-1,0),(-1,-1)]
def get_sum_list(a):
    d = [0]*3
    al = len(a)
    ail = len(a[0])
    l = [[0]*ail]*al
    for i in range(al):
        for j in range(ail):
            if not (i and j):
                continue
            for di in range(3):
                y = dxdy[di][0]
                x = dxdy[di][1]
                if (i+y) and (j+x):
                    d[di] = a[i+y][i+x]
            l[i][j] = l[i][j] + d[0] +d[1] -d[2]
    return l



print(get_sum_list(a))
        
