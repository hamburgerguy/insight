import numpy as np
import matplotlib.pyplot as plt

def quad(x):
    y = np.sqrt(x)
    return y

def lin(x):
    y = x
    return y

x = np.arange(100)


plt.plot(x,quad(x),label = 'quadratic')
plt.plot(x,lin(x), label = 'linear')
plt.legend()
plt.show()
