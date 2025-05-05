import sys
import time
import traceback
import os
import csv
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output, callback_context
from arduino_iot_cloud import ArduinoCloudClient
from threading import Thread, Lock
from datetime import datetime
import cv2
import base64
from io import BytesIO
from PIL import Image
import glob
import atexit
import random

DEVICE_ID = "fe565aeb-ea8b-4c56-8c6e-634e3eb7ca63"
SECRET_KEY = "hXrJ9LhZDn8FXpeyaoj1BLLEa"

# Constants
ACTIVITY_SPAN = (15, 20)
ACTIVITY_LABELS = {
    0: "no-activity",
    1: "waving",
    2: "shaking"
}

# Globals
lock = Lock()
recent_data = []
buffered_data = []
data_seq = 1
last_snapshot = time.time()
collecting = True
curr_action = 0
acc_x, acc_y, acc_z = None, None, None
start_time = time.time()
activity_timeframe = random.randint(*ACTIVITY_SPAN)

# Setup
os.makedirs('data', exist_ok=True)
os.makedirs('images', exist_ok=True)

camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Webcam failed to open")
    sys.exit(1)

# Initialize CSV if missing
if not os.path.exists('readings.csv'):
    with open('readings.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'activity'])

# Arduino Cloud Callbacks
def handle_x(client, value):
    global acc_x
    acc_x = value

def handle_y(client, value):
    global acc_y
    acc_y = value

def handle_z(client, value):
    global acc_z
    acc_z = value

def stream_sensor_data():
    global acc_x, acc_y, acc_z, buffered_data, recent_data
    try:
        cloud = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY, sync_mode=True)
        cloud.register("py_x", value=None, on_write=handle_x)
        cloud.register("py_y", value=None, on_write=handle_y)
        cloud.register("py_z", value=None, on_write=handle_z)
        cloud.start()

        while collecting:
            if acc_x is not None and acc_y is not None and acc_z is not None:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                row = [timestamp, acc_x, acc_y, acc_z]

                with lock:
                    recent_data.append(row)
                    buffered_data.append(row)
                    if len(recent_data) > 50:
                        recent_data.pop(0)

                acc_x = acc_y = acc_z = None

            cloud.update()

    except Exception:
        traceback.print_exc()

def auto_capture():
    global data_seq, last_snapshot, curr_action, start_time, activity_timeframe

    while collecting:
        now = time.time()

        if now - start_time >= activity_timeframe:
            curr_action = random.choice(list(ACTIVITY_LABELS.keys()))
            start_time = now
            activity_timeframe = random.randint(*ACTIVITY_SPAN)
            print(f"Now performing: {ACTIVITY_LABELS[curr_action]}")

        if now - last_snapshot >= 1:
            last_snapshot = now
            if not buffered_data:
                continue

            tag = datetime.now().strftime("%Y%m%d%H%M%S")
            label = f"{data_seq}_{tag}"

            try:
                # Save CSV
                with open(f"data/{label}.csv", 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Timestamp', 'X', 'Y', 'Z'])
                    writer.writerows(buffered_data)

                # Capture image
                success, frame = camera.read()
                if success:
                    img_path = f"images/{label}.jpg"
                    cv2.imwrite(img_path, frame)

                    with lock:
                        with open('readings.csv', 'a', newline='') as rf:
                            writer = csv.writer(rf)
                            writer.writerow([label, curr_action])
            except Exception as e:
                print("Data capture error:", e)

            with lock:
                buffered_data.clear()
                data_seq += 1

        time.sleep(0.1)

def shutdown():
    global collecting
    collecting = False
    camera.release()
    cv2.destroyAllWindows()

atexit.register(shutdown)

# Dash App Setup
app = Dash(__name__)

app.layout = html.Div([
    html.H2("Accelerometer Activity Tracker"),
    html.Div([
        html.Div(id='activity-info', style={'fontSize': 24, 'fontWeight': 'bold'}),
        html.Div(id='time-left', style={'fontSize': 18}),
        html.Button("No Activity", id='btn-0', n_clicks=0),
        html.Button("Waving", id='btn-1', n_clicks=0),
        html.Button("Shaking", id='btn-2', n_clicks=0),
        html.Button("Stop", id='btn-stop', n_clicks=0, style={'backgroundColor': 'red', 'color': 'white'})
    ]),
    dcc.Graph(id='accel-graph'),
    html.Img(id='live-img', style={'height': '300px'}),
    dcc.Interval(id='interval', interval=1000),
    html.Div(id='msg')
])

@app.callback(
    [Output('accel-graph', 'figure'),
     Output('live-img', 'src'),
     Output('activity-info', 'children'),
     Output('time-left', 'children'),
     Output('msg', 'children')],
    Input('interval', 'n_intervals')
)
def refresh(n):
    global start_time, activity_timeframe
    remaining = max(0, activity_timeframe - (time.time() - start_time))
    act_name = ACTIVITY_LABELS[curr_action]
    timer_msg = f"{remaining:.1f}s remaining for {act_name}"

    with lock:
        if not recent_data:
            return go.Figure(), "", f"Current: {act_name}", timer_msg, "No data yet"

        ts, x_vals, y_vals, z_vals = zip(*recent_data)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ts, y=x_vals, name='X', mode='lines'))
        fig.add_trace(go.Scatter(x=ts, y=y_vals, name='Y', mode='lines'))
        fig.add_trace(go.Scatter(x=ts, y=z_vals, name='Z', mode='lines'))

    latest_imgs = sorted(glob.glob(f"images/{data_seq-1}_*.jpg"))
    if latest_imgs:
        with open(latest_imgs[-1], 'rb') as f:
            img_data = base64.b64encode(f.read()).decode()
            img_src = f"data:image/jpeg;base64,{img_data}"
    else:
        img_src = ""

    return fig, img_src, f"Current: {act_name}", timer_msg, f"Last capture: {data_seq-1}"

@app.callback(
    [Output('btn-0', 'n_clicks'),
     Output('btn-1', 'n_clicks'),
     Output('btn-2', 'n_clicks')],
    [Input('btn-0', 'n_clicks'),
     Input('btn-1', 'n_clicks'),
     Input('btn-2', 'n_clicks')]
)
def set_manual(n0, n1, n2):
    global curr_action, start_time, activity_timeframe
    clicked = callback_context.triggered[0]['prop_id'].split('.')[0]
    if clicked == 'btn-0': curr_action = 0
    elif clicked == 'btn-1': curr_action = 1
    elif clicked == 'btn-2': curr_action = 2
    start_time = time.time()
    activity_timeframe = random.randint(*ACTIVITY_SPAN)
    return [0, 0, 0]

@app.callback(
    Output('interval', 'disabled'),
    Input('btn-stop', 'n_clicks')
)
def stop_everything(n):
    global collecting
    if n > 0:
        collecting = False
        shutdown()
        return True
    return False

if __name__ == '__main__':
    Thread(target=stream_sensor_data, daemon=True).start()
    Thread(target=auto_capture, daemon=True).start()
    app.run_server(debug=True, port=8050)
