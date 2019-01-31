import numpy as np
import matplotlib.pyplot as plt

x_values = []
for i in range(0,10000):
	x_values.append(i/10tre00)
y_values = []
for x in x_values:
	if x <= 5:
		y_values.append(x)
	else:
		y_values.append(np.e**(-x+5)+4)
plt.scatter(x_values, y_values, s=5)
plt.xticks([])
plt.yticks([])
plt.show()