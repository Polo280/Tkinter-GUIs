import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import floor
import time
import random

count = 0
start_time = time.time()
fig = plt.figure(figsize=([7, 5]))
plt.suptitle('Cansat data', fontsize=19, fontweight='bold')

# Plot 1
o3x = []
o3y = []
plt.subplot(2, 1, 1)

# Plot 2
humx = []
humy = []
plt.subplot(2, 1, 2)
plt.title('Humidity', pad=5)
plt.ylabel("Hum %")
plt.xlabel('Time')
plt.tight_layout()

def animate(i, xs:[], ys:[], xs2:[], ys2:[]):
    current_time = floor(time.time() - start_time)
    ys.append(random.randint(1, 100))
    xs.append(current_time)

    # Lists for data
    xs = xs[-100:]
    ys = ys[-100:]

    plt.subplot(2, 1, 1)
    plt.cla()              # Clears all data, including labels and titles
    plt.title('MQ-131')
    plt.ylabel('Ozone PPM')
    plt.xlabel('Time')
    print(xs)
    plt.plot(xs, ys)


    xs2 = xs2[-10:]
    ys2 = ys2[-10:]
    plt.subplot(2, 1, 2)
    plt.tight_layout()


#plt.suptitle("Test")
ani = animation.FuncAnimation(fig, animate, fargs=(o3x, o3y, humx, humy), interval=5000)  # Use interval for delay, DONT USE SLEEP
plt.show()
