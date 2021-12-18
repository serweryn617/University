# Ant algorithm
# Seweryn Rusecki & Nikodem Bartnik

# Solving travelling salesman problem with ant algorithm.
# Coordinates of cities are specified in x and y vectors.

# Exemplary Result:
# Length: 43.629476033689144
# Order: [7 4 8 9 1 5 0 3 2 6 7]

# Libraries
import numpy as np

# Timing
import time

start_time = time.time()

# Parameters
T_MAX = 100 # Number of iterations
ANTS_NUMBER = 10 # Ants per iteration

# Cities (set 4)
x = [3, 2, 12,   7, 9,   3, 16, 11,  9, 2]
y = [1, 4,  2, 4.5, 9, 1.5, 11,  8, 10, 7]

# Distance functions
def totalDist(px, py, ord):
    d = 0
    for i in range(len(ord) - 1):
        d += calcDist(px, py, ord[i], ord[i + 1])
    return d

def calcDist(px, py, i, j):
    return ((px[i] - px[j])**2+(py[i] - py[j])**2)**0.5

# Variables
l = len(x)
ants = np.zeros([ANTS_NUMBER, l+1], dtype='int') - 1
ants_d = np.zeros(ANTS_NUMBER)
min_dist = 0
min_ord = []

# Distances
d = np.zeros((l,l))
for xx in range(l):
    for yy in range(l):
        d[xx,yy] = (((x[xx] - x[yy])**2+(y[xx] - y[yy])**2)**0.5)
        if xx == yy:
            d[xx,yy] = 1

d_max = np.max(d)

# Initial pheromone
τ = np.zeros((l,l)) + 1/d_max

# Parameters
α = 1
β = 5
ρ = 0.5
η = 1/d

# Split ants randomly into 10 cities
ants[:,0] = np.random.randint(0, l-1, ANTS_NUMBER)

# Main loop
for _ in range(T_MAX):
    # At the beginning clear result from previous iteration
    ants[:, 1:] = -1

    for k in range(ANTS_NUMBER):
        for city_loop in range(l):
            # Extract visited and not visited cities from ants array
            cities_visited = np.delete(ants[k, :], np.where(ants[k,:] == -1)) # skip -1
            not_visited = np.delete(np.arange(l), (cities_visited)) # all cities except visited
            
            # Current city
            i = cities_visited[-1] # Current city is the city last visited

            # In the last step, ant has to get back to starting location
            if len(not_visited) == 0:
                not_visited = [cities_visited[0]]
                
            # Decision table
            a = np.zeros((len(not_visited)))
            for j in range(len(not_visited)):
                s=0
                for z in not_visited:
                    s += τ[int(i),int(z)]**α * η[int(i),int(z)]**β
                a[j] = (τ[int(i),not_visited[j]]**α * η[int(i),not_visited[j]]**β) / s

            # Probabilities
            p = a / np.sum(a)

            # Choose path
            rand = np.random.uniform() # Generate random number
            sum = p[0] # Start from probability of first path
            itr = 0

            # Fitness proportionate selection
            while sum < rand:
                itr += 1    
                sum += p[itr]

            # Save where the ant goes
            ants[k, city_loop + 1] = not_visited[itr]

        # Save total distance after an ant has made the journey
        ants_d[k] = totalDist(x, y, ants[k])

    # If result is better than current best, update it
    min_idx = np.argmin(ants_d)
    if ants_d[min_idx] < min_dist or _ == 0:
        min_dist = ants_d[min_idx]
        min_ord = np.copy(ants[min_idx])
    
    # Update pheromone (τ) after all ants went through all cities
    τ *= 1 - ρ
    for k in range(len(ants)):
        for c in range(len(ants[k]) - 1):        
            τ[ants[k][c]][ants[k][c + 1]] += 1/ants_d[k]
            τ[ants[k][c + 1]][ants[k][c]] += 1/ants_d[k]

# Print out the result
print('Length:', min_dist)
print('Order:', min_ord)

# Print execution time
print('Time', int((time.time() - start_time) * 1000), 'ms')

# Plot
from plot import NetPlot
net = NetPlot(x, y)
net.addOrder(min_ord)
net.plotCities(True)
net.show()