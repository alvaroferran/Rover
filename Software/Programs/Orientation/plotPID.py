import matplotlib.pyplot as plt
import numpy as np

fileName = "data"
x, y = np.loadtxt(fileName, delimiter=';', unpack=True)

plt.plot(x, y)
plt.xlabel('Time (s)')
plt.ylabel('Angle (degrees)')
plt.title('PD graph')
plt.grid(True)
plt.savefig("pid.png")
plt.show()
