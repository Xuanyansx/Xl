def input_d():
    return input().split()

def zhang_cao(map_data,n,m):
    d = [
        (-1,0),
    (0,-1),(0,1),
        (1,0),
    ]
    
    for y in range(n):
        if 'g' not in map_data[y]:
            if 'G' in map_data[y]:
                map_data[y] = [i if i!='G' else 'g' for i in map_data[y]]
            continue
        for x in range(m):
            if map_data[y][x] == 'g':
                for i in range(4):
                    yi = y+d[i][0]
                    xi = x+d[i][1]
                    if 0<=yi<n and 0<=xi<m and map_data[yi][xi] == '.':
                        map_data[yi][xi] = 'G' if i>0 else 'g'
        map_data[y] = [i if i!='G' else 'g' for i in map_data[y]]

   

n,m = list(map(int,input_d()))

map_data = []
for i in range(n):
    map_data.append(list(input_d()[0]))

k = int(input())

for i in range(k):
    zhang_cao(map_data,n,m)


for i in map_data:
    print(''.join(i))