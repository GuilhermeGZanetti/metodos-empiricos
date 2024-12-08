import matplotlib.pyplot as plt
import numpy as np


def my_function(x):
    return 0.8 * x + 1.5 

# Generate some random data around a linear trend
np.random.seed(0)
x = np.linspace(0.5, 2.0, 20)
y = my_function(x) + np.random.normal(scale=0.1, size=len(x))

# Create the plot
plt.figure(figsize=(6, 6))
plt.scatter(x, y, color='black', s=20)  # Scatter plot
plt.plot(x, my_function(x), color='black', linewidth=1)  # Linear trend line

# Labeling the axes
plt.xlabel("γ")
plt.ylabel("C")

# Set limits to match the image
plt.xlim(0.5, 2.0)
plt.ylim(1.8, 3.0)

# Adjusting ticks
plt.xticks(np.arange(0.5, 2.0, 0.5))
plt.yticks(np.arange(1.8, 3.2, 0.2))

plt.grid(False)
plt.tight_layout()
# Save to file
plt.savefig("linear_regression.png", dpi=300)
plt.show()
