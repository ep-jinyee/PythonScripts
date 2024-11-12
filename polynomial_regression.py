import numpy as np
import matplotlib.pyplot as plt

# Sample datasets
data = [
    [3145, 1684, 1999, 1259, 2228, 1349, 1546, 1063, 2422, 1416, 1632, 1102, 1781, 1170, 1314, 946],
    [3155, 1674, 1992, 1250, 2225, 1339, 1536, 1052, 2417, 1402, 1622, 1092, 1773, 1160, 1304, 935],
    [3145, 1633, 1944, 1213, 2181, 1302, 1499, 1021, 2372, 1367, 1584, 1060, 1738, 1128, 1271, 906],
    [3065, 1664, 1982, 1242, 2234, 1331, 1530, 1047, 2411, 1408, 1615, 1077, 1771, 1156, 1300, 929]
]

# Create an array for x values (indices)
x = np.arange(len(data[0]))

# Plotting
plt.figure(figsize=(10, 6))
plt.subplot(2,1,1);
plt.plot(x, data[1], marker='s', linestyle='--', color='r', label='FP 1')
plt.plot(x, data[0], marker='o', linestyle='-', color='b', label='FP 2')
plt.plot(x, data[3], marker='+', linestyle=':', color='#000', label='MP 1')
plt.plot(x, data[2], marker='p', linestyle=':', color='g', label='MP 2')

plt.subplot(2,1,1);
plt.plot(x, data[1], marker='s', linestyle='--', color='r', label='FP 1')
plt.plot(x, data[0], marker='o', linestyle='-', color='b', label='FP 2')
plt.plot(x, data[3], marker='+', linestyle=':', color='#000', label='MP 1')
plt.plot(x, data[2], marker='p', linestyle=':', color='g', label='MP 2')
# Adding title and labels
plt.title('Comparison of DIP Switch and their ADC Value of Different Board')
plt.xlabel('ADC Address')
plt.ylabel('ADC Value (mV)')
plt.xticks(x)  # Set x-ticks to match the indices
plt.grid(True)
plt.legend()  # Show legend
plt.show()


# Sample data
x = np.arange(10)
y = np.random.rand(10) * 100  # Random values

# Calculate mean, max, and min
mean_y = np.mean(y)
max_y = np.max(y)
min_y = np.min(y)

# Create the plot
plt.figure(figsize=(10, 5))
plt.plot(x, y, marker='o', linestyle='-', color='blue', label='Data')

# Plotting mean, max, and min
plt.axhline(mean_y, color='green', linestyle='--', label='Mean')
plt.axhline(max_y, color='red', linestyle='--', label='Max')
plt.axhline(min_y, color='orange', linestyle='--', label='Min')

# Adding title and labels
plt.title('Data with Mean, Max, and Min')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()