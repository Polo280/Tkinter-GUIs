# Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np

#Change the figure size
plt.figure(figsize=[11, 9])

# Preparing the data to subplots
x = np.linspace(0, 10, 10)
y1 = x
y2 = x ** 2
y3 = x ** 3
y4 = x ** 4

plt.suptitle('Different degree curves')

# Plot the subplots
# Plot 1
plt.subplot(2, 2, 1)
plt.plot(x, y1, 'g', linewidth=2)
plt.title('Plot 1: 1st Degree curve')

# Plot 2
plt.subplot(2, 2, 2)
plt.scatter(x, y2, color='k')
plt.title('Plot 2: 2nd Degree curve')

# Plot 3
plt.subplot(2, 2, 3)
plt.plot(x, y3, '-.y', linewidth=3)
plt.title('Plot 3: 3rd Degree curve')

# Plot 4
plt.subplot(2, 2, 4)
plt.plot(x, y4, '--b', linewidth=3)
plt.title('Plot 4: 4th Degree curve')

plt.show()