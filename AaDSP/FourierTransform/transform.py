# Periodic signal expansion into fourier series

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Parameters
filepath = 'func.csv'
num_coeff = 50 # For higher values there are some floating point arithmetic errors
draw_periods = 2
points = 10000

# Import csv
data = np.genfromtxt(filepath, delimiter=',')

# Variables
vals = data[:, 1]
args = data[:, 0]
period = args[-1]
ω = 2*np.pi/period

# # Predefined Functions
# I1 = 1
# I3 = 3
# N2 = 2

# Am = 2*I1
# # Start with updating ω and T
# ω = 100*I3 + 10*N2
# period = 2*np.pi/ω

# # End predefined function with args and vals
# args = np.linspace(period/points, period, 1000)
# # Actual function
# vals = Am * np.sin(ω * args)
# # End of predefined function

# Calculate step and mean value
Δ = args[0]
mean_val = np.mean(vals)
vals = np.subtract(vals, mean_val)

# Calculate Fourier series coefficients as:
#   ak = 2/T * integral from 0 to T of: f(t)*cos(k ω0 t) dt
#   bk = 2/T * integral from 0 to T of: f(t)*sin(k ω0 t) dt
a_coeff = []
b_coeff = []

for k in range(1, num_coeff + 1):
    a_coeff.append(2 / period * Δ * np.sum(np.multiply(vals, np.cos(k*ω*args))))
    b_coeff.append(2 / period * Δ * np.sum(np.multiply(vals, np.sin(k*ω*args))))

# Arguments for plotting the reconstructed signal
rargs = np.linspace(0, draw_periods * period, points)

ak = np.array(a_coeff)[np.newaxis]
bk = np.array(b_coeff)[np.newaxis]



# Plotting

# The parametrized function to be plotted
def f(numc):
    a2 = np.array(a_coeff[0:numc])[np.newaxis]
    b2 = np.array(b_coeff[0:numc])[np.newaxis]
    c = np.array(range(1, numc + 1))[np.newaxis]
    y1 = np.sum(a2.T * np.cos(rargs*c.T*ω), 0)
    y2 = np.sum(b2.T * np.sin(rargs*c.T*ω), 0)
    return y1 + y2 + mean_val

# Initial parameters
init_k = num_coeff

# Create the figure and line to manipulate
fig, ax = plt.subplots()
line, = plt.plot(rargs, f(init_k), lw=1, label='Fourier reconstruction')
plt.plot(args, vals + mean_val, label='Original signal')
legend = ax.legend(loc='upper right', shadow=True, fontsize='small')
ax.set_xlabel('Time [s]')

axcolor = 'lightgoldenrodyellow'
ax.margins(x=0)

# Adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25)

# Make a vertically oriented slider to control the amplitude
axamp = plt.axes([0.1, 0.25, 0.0225, 0.63], facecolor=axcolor)
c_slider = Slider(
    ax=axamp,
    label="k",
    valmin=0,
    valmax=num_coeff,
    valinit=init_k,
    valstep=1,
    orientation="vertical"
)

# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata(f(int(c_slider.val)))
    fig.canvas.draw_idle()

# Call a function on slider's value change
c_slider.on_changed(update)

plt.show()
