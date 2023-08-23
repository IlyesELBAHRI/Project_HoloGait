import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Read the csv file
df = pd.read_csv('AR_Environment/Replay_HoloGait_App/testV3.csv')

# Extract position information
Gaze_Origin_x = df['Gaze_Origin.x'].values
Gaze_Origin_z = df['Gaze_Origin.z'].values
Gaze_Origin_y = df['Gaze_Origin.y'].values
gaze_direction = df[['Gaze_Direction.x', 'Gaze_Direction.y', 'Gaze_Direction.y']].values
head_movement_direction = df[['Head_Movement_Direction.x', 'Head_Movement_Direction.y', 'Head_Movement_Direction.z']].values
head_velocity = df[['Head_Velocity.x', 'Head_Velocity.y', 'Head_Velocity.z']].values
hit_position = df[['Hit_Position.x', 'Hit_Position.y', 'Hit_Position.z']].values
cursor_position = df[['Cursor_Position.x', 'Cursor_Position.y', 'Cursor_Position.z']].values

# Create a 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
line, = ax.plot3D(Gaze_Origin_z, Gaze_Origin_x, Gaze_Origin_y, '-b')  # Initial plot of the path
point, = ax.plot3D([], [], [], 'ro', markersize=6)  # Empty plot for the moving point
gaze_line, = ax.plot3D([], [], [], '-g', linewidth=1)  # Empty plot for the gaze direction line

# Set the title and the labels
ax.set_title('Path Traveled by the User')
ax.set_xlabel('Depth (Z)')
ax.set_ylabel('X')
ax.set_zlabel('Y')

# Invert the y-axis to match the usual coordinate system
ax.invert_yaxis()

# Animation function to update the position and color of the moving point and the gaze direction line
def update(i):
    index = i + 1000  # Skip the first 1000 values
    line.set_data(Gaze_Origin_z[:index], Gaze_Origin_x[:index])
    line.set_3d_properties(0)
    point.set_data([Gaze_Origin_z[index]], [Gaze_Origin_x[index]])
    point.set_3d_properties(0)
    gaze_length = 0.8  # Length of the gaze direction line
    gaze_end_x = Gaze_Origin_x[index] + gaze_length * gaze_direction[index, 0]
    gaze_end_z = Gaze_Origin_z[index] + gaze_length * gaze_direction[index, 2]
    gaze_line.set_data([Gaze_Origin_z[index], gaze_end_z], [Gaze_Origin_x[index], gaze_end_x])
    gaze_line.set_3d_properties(0)

# Create the animation
ani = FuncAnimation(fig, update, frames=len(Gaze_Origin_x)-1000, interval=100, repeat=True)

# Show the plot
plt.show()