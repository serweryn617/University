# Seweryn Rusecki
# AI lab 8

# Genetic algorithm
# Approximating coefficients a, b, c
# in function f(i) = a*(i^2 - b*cos(c*π*i))
# from which sample points are given

# This is a simplified genetic algorithm, where
# the only variation introduced to new generation
# is mutation. Normally used recombination is not
# present.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Parameters
filepath = 'samples.dat'
pop_size = 100
offspring_num = 5
num_coefficients = 3
max_iterations = 200
ε = 0.0001
output_resolution = 0.001

# Load data
sampled_data = np.genfromtxt(filepath, autostrip=True)

# Calculate τ1 and τ2
τ1 = 1/np.sqrt(2*num_coefficients)
τ2 = 1/np.sqrt(2 * np.sqrt(num_coefficients))

# Containers for results from each generation
res_mse = []
res_a = []
res_b = []
res_c = []

# Generate random population
pop = np.concatenate((np.zeros((pop_size,1)), np.random.rand(pop_size, 3)*20-10, np.random.rand(pop_size, 3)*10), 1)
prev_mse = 0

for itr in range(max_iterations):
    # MSE
    for n in range(pop_size * offspring_num if itr != 0 else pop_size):
        pop[n,0] = np.mean(np.square(sampled_data[:,1] - pop[n,1]*(np.square(sampled_data[:,0]) - pop[n,2]*np.cos(pop[n,3]*np.pi*sampled_data[:,0]))))

    # Sort offsprings
    pop = pop[np.argsort(pop[:,0])]
    
    # Select best
    pop = pop[0:pop_size,:]
    
    # Print and save
    print(itr, "MSE:", pop[0,0])
    res_mse.append(pop[0,0])
    res_a.append(pop[0,1])
    res_b.append(pop[0,2])
    res_c.append(pop[0,3])
    mse = pop[0,0]

    # End condition
    if abs(mse - prev_mse) < ε:
        break
    prev_mse = mse

    # Duplicate each row 5 times (offspring num) and set first column to zeros
    pop = np.concatenate((np.zeros((pop_size * offspring_num, 1)), np.repeat(pop[:,1:7], offspring_num, 0)), 1)
    
    # Create r  matrix
    r = np.random.normal(0,1,(pop_size * offspring_num,3))
    
    # Create r1 matrix
    r1 = np.repeat(np.random.normal(0,1,(pop_size * offspring_num,1)) * τ1, 3, 1)
    
    # Create r2 matrix
    r2 = np.random.normal(0,1,(pop_size * offspring_num,3)) * τ2
    
    # Generate a,b,c as: a1 = a0 + r*Sigma_a
    pop[:,1:4] = pop[:,1:4] + r * pop[:,4:7]
    
    # Generate σ as: σ1 = σ0 * exp(r1) * exp(r2)
    pop[:,4:7] = pop[:,4:7] * np.exp(r1) * np.exp(r2)


# Print result
print("a =", res_a[-1], "\nb =", res_b[-1], "\nc =", res_c[-1])



# Plot

# Plot parameters
xmore = np.arange(-5, 5, output_resolution)

# The parametrized function to be plotted
def f(numc):
    yp = res_a[numc]*(np.square(xmore) - res_b[numc] * np.cos(res_c[numc]*np.pi*xmore))
    return yp

# Initial parameters
init_n = itr

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = plt.plot(xmore, f(init_n), lw=2)
ax.set_xlabel('i')
ax.set_ylabel('o')
ax.set_title('o = f(i)')

axcolor = 'lightgoldenrodyellow'
ax.margins(x=0)

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25)

# Make a vertically oriented slider to control the amplitude
axamp = plt.axes([0.1, 0.28, 0.0225, 0.6], facecolor=axcolor)
n_slider = Slider(
    ax=axamp,
    label="n",
    valmin=0,
    valmax=itr,
    valinit=init_n,
    valstep=1,
    orientation="vertical"
)

# Text boxes
fig.text(0.1, 0.2, 'MSE: ', ha="right", size=11)
tm = fig.text(0.1, 0.2, round(res_mse[-1], 4), size=11)
fig.text(0.1, 0.16, 'a: ', ha="right", size=11)
ta = fig.text(0.1, 0.16, round(res_a[-1], 4), size=11)
fig.text(0.1, 0.12, 'b: ', ha="right", size=11)
tb = fig.text(0.1, 0.12, round(res_b[-1], 4), size=11)
fig.text(0.1, 0.08, 'c: ', ha="right", size=11)
tc = fig.text(0.1, 0.08, round(res_c[-1], 4), size=11)

# The function to be called anytime slider's value changes
def update(val):
    line.set_ydata(f(int(n_slider.val)))
    fig.canvas.draw_idle()
    tm.set_text(round(res_mse[int(n_slider.val)], 4))
    ta.set_text(round(res_a[int(n_slider.val)], 4))
    tb.set_text(round(res_b[int(n_slider.val)], 4))
    tc.set_text(round(res_c[int(n_slider.val)], 4))

# Call update function
n_slider.on_changed(update)

# Add target plot
ax.plot(sampled_data[:,0],sampled_data[:,1], 'r+', lw=1)
ax.plot(sampled_data[:,0],sampled_data[:,1], color='red', lw=1)
plt.show()
