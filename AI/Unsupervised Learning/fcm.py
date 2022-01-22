# FCM algorithm
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

# Dimension
dim = len(fileArray[0])
print('Dim', dim)

# Parameters
c = 3
e = 0.00001
m = 1.1

# Criterion
prev_sum = 0
iteration = 0

# Partition matrix c by N, contains vallues from 0 to 1
partition = [[random.random() for x in range(c)] for y in range(N)]
for x in range(N):
    sum = 0
    for y in range(c):
        sum += partition[x][y]
    for y in range(c):
        partition[x][y] /= sum

# Partition to example 4
# partition = [[0.5, 0.5],[0.7, 0.3],[0.0, 1.0],[0.0, 1.0],[1.0, 0.0],[0.4, 0.6],[0.6, 0.4],[0.2, 0.8],[]]

while True:
    total_positions = [[0 for d in range(dim)] for _ in range(c)] #x,y,z....
    total_points = [0 for _ in range(c)]

    for x in range(N):
        for y in range(c):
            for d in range(dim):
                total_positions[y][d] += fileArray[x][d] * (partition[x][y])**m
            total_points[y] += (partition[x][y])**m

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
            sum += distances[x][y] * (partition[x][y])**m
        
    print('Sum of distances:', sum)
    if abs(sum - prev_sum) < e:
        break
    prev_sum = sum
        
    partition = [[0 for x in range(c)] for y in range(N)]
    for i, dis in enumerate(distances):
        if min(dis) == 0:
            partition[i][dis.index(min(dis))] = 1
        else:
            dissum = 0
            for d in dis:
                dissum += d**(1/(1-m))
            for j, d in enumerate(dis):
                partition[i][j] = (d**(1/(1-m)))/dissum
    
    iteration += 1
    print('\nIteration', iteration)
    print('Partition matrix:', partition)
plot.plot(fileArray, partition, total_positions, sum)