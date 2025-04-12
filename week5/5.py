import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV
df = pd.read_csv(r'D:\python\week5\xyz.csv')

if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    x_axis = df['timestamp']
else:
    x_axis = df.index

# Plot X
plt.figure(figsize=(10, 4))
plt.plot(x_axis, df['x'], color='r')
plt.title('Gyroscope X over Time')
plt.xlabel('Time')
plt.ylabel('X Value')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot Y
plt.figure(figsize=(10, 4))
plt.plot(x_axis, df['y'], color='g')
plt.title('Gyroscope Y over Time')
plt.xlabel('Time')
plt.ylabel('Y Value')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot Z
plt.figure(figsize=(10, 4))
plt.plot(x_axis, df['z'], color='b')
plt.title('Gyroscope Z over Time')
plt.xlabel('Time')
plt.ylabel('Z Value')
plt.grid(True)
plt.tight_layout()
plt.show()

# Combined Plot
plt.figure(figsize=(12, 5))
plt.plot(x_axis, df['x'], label='X', color='r')
plt.plot(x_axis, df['y'], label='Y', color='g')
plt.plot(x_axis, df['z'], label='Z', color='b')
plt.title('Combined Gyroscope Data')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

