import serial
import random
import time
from datetime import datetime

ser = serial.Serial('COM15', 9600)  
time.sleep(2)  

while True:
    random_number = random.randint(1, 10)  
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
    ser.write(str(random_number).encode())  
    print(f"{timestamp} - Sent: {random_number}")
    response = ser.readline().decode().strip()  
    print(f"{timestamp} - Received: {response}")  
    time.sleep(int(response))  
    print(f"{timestamp} - Sleeping for {response} seconds")






























# import serial
# import random

# # set baud rate, same speed as set in your Arduino sketch.
# boud_rate = 9600

# # set serial port as suits your operating system
# s = serial.Serial('/dev/ttyACM1', boud_rate, timeout=5)

# while True:  # infinite loop, keep running

#     #  a random number between 5 and 50.
#     data_send = random.randint(5, 50)

#     # write to serial port, set data encoding. 
#     # Raw bytes are sent through serial ports, Python bytes() needs 
#     # to know the encoding to generate bytes from string.
#     # 
#     # We send a single integer which is read from Arduino sketch.
#     # 
#     d = s.write(bytes(str(data_send), 'utf-8'))
#     print(f"Send >>> {data_send} ({d} bytes)")

#     # Read from serial port. 
#     # 
#     # readline keeps reading until a newline found in the data stream.
#     # Unlike write above, we just send an integer with no newline.
#     # You should receive data the same way as it is sent.
#     # 
#     d = s.readline().decode("utf-8")
#     print(f"Recv <<< {d}")