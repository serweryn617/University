# HCM and FCM plottiong
#   Nikodem Bartnik
#   Seweryn Rusecki
from matplotlib import pyplot as plt

def plot(data, u, c, j):
    dx = [[] for _ in range(len(u[0]))]
    dy = [[] for _ in range(len(u[0]))]

    for i in range(len(u)):
        dx[u[i].index(max(u[i]))].append(data[i][0])
        dy[u[i].index(max(u[i]))].append(data[i][1])

    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111)
    ax.set_position([0.1, 0.3, 0.8, 0.6])

    for d in range(len(dx)):
        plt.plot(dx[d], dy[d], 'o', linewidth=0, label=f"Ω = {[round(ui[d], 2) for ui in u]}")
    plt.gca().set_prop_cycle(None)
    for p in c:
        plt.plot(p[0], p[1], 'x', linewidth=0)
    plt.plot(5,5,color='white', label=f"J = {j}")

    plt.legend(loc='upper left', bbox_to_anchor=(0, -0.06))
    plt.show()