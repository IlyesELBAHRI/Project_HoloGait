import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Read the csv file
df = pd.read_csv('AR_Environment/Replay_HoloGait_App/testV2.csv', delimiter=',')

# Extract gaze information
gaze_origin = df[['Gaze_Origin.x', 'Gaze_Origin.y', 'Gaze_Origin.z']].values
time = df['Time'].values

# Create a 3D graph
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Parameters for the cylinder
radius = 0.1
height = 0.2
resolution = 50

# Generate cylinder coordinates
theta = np.linspace(0, 2 * np.pi, resolution)
z_cylinder_coords = np.linspace(0, height, resolution)
theta, z_cylinder_coords = np.meshgrid(theta, z_cylinder_coords)

# Repeat gaze_origin for each cylinder coordinate
x_cylinder = np.tile(gaze_origin[:, 0], (resolution, 1)).T
y_cylinder = np.tile(gaze_origin[:, 1], (resolution, 1)).T
z_cylinder = np.tile(gaze_origin[:, 2, np.newaxis], (1, resolution)) + np.broadcast_to(z_cylinder_coords, (len(gaze_origin), resolution))

# Plot the cylinder at each gaze position
for i in range(len(gaze_origin)):
    ax.plot_surface(x_cylinder[i], y_cylinder[i], z_cylinder[i], alpha=0.5)

# Set the title and the labels
ax.set_title('Patient Position Over Time')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the graph
plt.show()
