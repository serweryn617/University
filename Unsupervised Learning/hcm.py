# HCM algorithm
#   Nikodem Bartnik
#   Seweryn Rusecki
import plot
import random

def calcDist(p1, p2):
    dist = 0
    for x in range(len(p1)):
        dist += (p1[x] - p2[x])**2
    return dist

# Opening data file
file = open('test_data.txt')
fileArray = []
for line in file:
    fileArray.append(line.strip().split(','))

for line in range(len(fileArray)):
    for elem in range(len(fileArray[0])):
        fileArray[line][elem] = float(fileArray[line][elem])

# N objects
N = len(fileArray)
print('Length', N)

# dimension
dim = len(fileArray[0])
print('Dim', dim)

# Parameters
c = 2
e = 0.00001

# Criterion
prev_sum = 0
iteration = 0

# Partition matrix c by N, contains 0 or 1
partition = [[0 for x in range(c)] for y in range(N)]
for r in range(N):
    rand_n = random.randint(0, c - 1)
    partition[r][rand_n] = 1
print(partition)

# Partition to example 4
# partition = [[1,0], [1,0], [0,1], [0,1], [1,0], [0,1], [1,0], [0,1]]

while True:
    total_positions = [[0 for d in range(dim)] for _ in range(c)] #x,y,z....
    total_points = [0 for _ in range(c)]

    for x in range(N):
        for y in range(c):
            if partition[x][y]:
                for d in range(dim):
                    total_positions[y][d] += fileArray[x][d]
                total_points[y] += 1
                break

    for x in range(c):
        for d in range(dim):
            total_positions[x][d] /= total_points[x]
    print('Centers', total_positions)

    distances = []
    for x in range(N):
        distances.append([])
        for y in range(c):
            distances[-1].append(calcDist(fileArray[x], total_positions[y]))

    sum = 0
    for x in range(len(distances)):
        for y in range(len(distances[0])):
            if partition[x][y]:
                sum += distances[x][y]
        
    print('Sum of distances:', sum)
    if abs(sum - prev_sum) < e:
        break
    prev_sum = sum
      
    partition = [[0 for x in range(c)] for y in range(N)]
    for i, dis in enumerate(distances):
        partition[i][dis.index(min(dis))] = 1
    
    iteration += 1
    print('Iteration', iteration)
plot.plot(fileArray, partition, total_positions, sum)