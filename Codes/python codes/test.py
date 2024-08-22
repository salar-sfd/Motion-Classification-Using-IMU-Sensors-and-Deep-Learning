import matplotlib.pyplot as plt
import numpy as np
import time

# Enable interactive mode
plt.ion()

# Create initial figures and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Initial data
x = np.linspace(0, 2 * np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Plot initial data
line1, = ax1.plot(x, y1, label='sin(x)')
line2, = ax2.plot(x, y2, label='cos(x)')

# Set labels
ax1.set_title('Sine Wave')
ax1.set_xlabel('x')
ax1.set_ylabel('sin(x)')
ax1.legend()

ax2.set_title('Cosine Wave')
ax2.set_xlabel('x')
ax2.set_ylabel('cos(x)')
ax2.legend()

# Show the plot
plt.show()

# Update data in a loop
for i in range(100):
    # Update data
    y1 = np.sin(x + i * 0.1)
    y2 = np.cos(x + i * 0.1)

    # Update lines
    line1.set_ydata(y1)
    line2.set_ydata(y2)

    # Adjust axis limits if needed
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()

    # Pause for a short time
    plt.pause(0.1)

# Disable interactive mode
plt.ioff()
