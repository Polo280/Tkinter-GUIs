import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import floor
import random

start_time = time.time()
figure, axs = plt.subplots(2, 1, constrained_layout=True)            # Create a new plot window
plt.subplot(2, 1, 1)
plt.title('MQ-131')
plt.xlabel('Ozone')
xs = []
ys = []
xs2 = []
ys2 = []
count = 0


def animate(i, xs:[], ys:[], xs2:[], ys2:[]):
    global count
    count += 1
    current_time = floor(time.time() - start_time)

    xs.append(current_time)
    ys.append(random.randint(1, 100))

    xs2.append(current_time)
    ys2.append(count)

    xs = xs[-10:]
    ys = ys[-10:]

    xs2 = xs2[-10:]
    ys2 = ys2[-10:]

    axs[0].clear()
    axs[0].plot(xs, ys)

    axs[1].clear()
    axs[1].plot(xs2, ys2)

#plt.suptitle("Test")
ani = animation.FuncAnimation(figure, animate, fargs=(xs, ys, xs2, ys2), interval=5000)  # Use interval for delay, DONT USE SLEEP
plt.show()            # Show all plots