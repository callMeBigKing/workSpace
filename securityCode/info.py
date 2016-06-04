# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 1000)
y = np.sin(x)
z = np.cos(x**2)
plt.figure(figsize=(8,4))
# for i in range(100):
#     plt.plot(i,np.sin(i),label="$sin(x)$",color="red",linewidth=2)
# plt.show()
plt.plot(list(range(1000)),list(range(1000)))
plt.plot(x,z,"b--")
plt.xlabel("Time(s)")
plt.ylabel("Volt")
plt.title("PyPlot First Example")
plt.ylim(-1.2,1.2)
plt.legend()
plt.show()