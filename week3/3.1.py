# """
# Requirement: arduino_iot_cloud
# Install: pip install arduino-iot-cloud

# @Ahsan Habib
# School of IT, Deakin University, Australia.
# """

# import csv
# import time
# from arduino_iot_cloud import ArduinoCloudClient

# # Cloud and file configurations
# DEVICE_ID = "bc5c0fe9-e6ef-4eb0-90de-05032ffd9a83"
# SECRET_KEY = "3oJYfrkmSNjM4YwKGJgVObbBn"
# CSV_FILE = "diksha.csv"


# def log_distance(value):
#     """Log distance readings to the CSV file with timestamps."""
#     timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
#     with open(CSV_FILE, mode='a', newline='') as file:
#         csv.writer(file).writerow([timestamp, value])
#     print(f"Data logged: {timestamp}, {value} cm")


# def main():
#     """Setup and run the data collection process."""
#     print("Starting data collection from Arduino IoT Cloud...")

#     # Create CSV with header
#     with open(CSV_FILE, mode='w', newline='') as file:
#         csv.writer(file).writerow(['Timestamp', 'Distance (cm)'])

#     # Setup and start Arduino Cloud client
#     client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
#     client.register("distance", value=0, on_write=lambda client, value: log_distance(value))
#     client.start()

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("\nData collection stopped by user.")


# if __name__ == "__main__":
#     main()






import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
csv_file = "diksha.csv"
df = pd.read_csv(csv_file)

# Convert 'Timestamp' column to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Plot the distance readings over time
plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['Distance (cm)'], marker='o', linestyle='-', color='b', label='Distance (cm)')

# Formatting the graph
plt.xlabel("Time")
plt.ylabel("Distance (cm)")
plt.title("Distance Readings Over Time")
plt.xticks(rotation=45)
plt.legend()
plt.grid()

# Show the graph
plt.show()








