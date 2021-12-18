
# Ant algorithm plot class

import matplotlib.pyplot as plt

class NetPlot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.orders = []

        # Create the figure and the line that we will manipulate
        self.fig, self.ax = plt.subplots()
        self.line = plt.plot(self.x, self.y, linewidth=0)

        self.axcolor = 'lightgoldenrodyellow'
        self.ax.margins(x=0)
        
        # adjust the main plot to make room for the sliders
        plt.subplots_adjust(left=0.25)
        self.tm = self.fig.text(0.11125, 0.1, round(1.11111, 4), size=11, ha='center')
        self.fig.text(0.11125, 0.15, 'Distance:', size=11, ha='center')



    def show(self):
        self.plotPath(0)
        self.tm.set_text(round(self.totalDist(-1), 4))

        plt.show()



    def addOrder(self, o):
        self.orders.append(o)



    def plotCities(self, show):
        plt.sca(self.ax) # set current axes
        self.line = plt.plot(self.x, self.y, 'o', linewidth=0, color='#ff0000', markersize=5)
        
        if(show):
            l = len(self.x)
            for ix in range(l):
                for iy in range(ix, l):
                    plt.plot((self.x[ix], self.x[iy]), (self.y[ix], self.y[iy]), 
                        linestyle=':',
                        color='#dddddd',
                    )
        
        c = 0
        for i_x, i_y in zip(self.x, self.y):
            plt.text(i_x + 0.1, i_y, '{}'.format(c), va="top")
            c += 1

        plt.xlim((min(self.x)-1, max(self.x)+1))
        plt.ylim((min(self.y)-1, max(self.y)+1))



    def plotPath(self, p):
        plt.sca(self.ax)

        # Lines
        self.line = plt.plot([self.x[i] for i in self.orders[p]], [self.y[i] for i in self.orders[p]])
        
        # Distances
        for t in range(len(self.orders[p]) - 1):
            plt.text(
                (self.x[self.orders[p][t]] + self.x[self.orders[p][t + 1]]) / 2,
                (self.y[self.orders[p][t]] + self.y[self.orders[p][t + 1]]) / 2,
                '{}'.format(round(self.calcDist(self.orders[p][t], self.orders[p][t + 1]), 2)), va="center", ha='center'
            )



    def calcDist(self, i, j):
        return ((self.x[i] - self.x[j])**2+(self.y[i] - self.y[j])**2)**0.5



    def totalDist(self, ord):
        d = 0
        for i in range(len(self.orders[ord]) - 1):
            d += self.calcDist(self.orders[ord][i], self.orders[ord][i + 1]) # if i + 1 < len(self.x) else 0
        return d