import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import os

CSV_FILE = 'accel_data.csv'  

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Smooth Live Accelerometer Data'),

    dcc.Graph(id='live-graph', style={'height': '70vh'}),

    dcc.Interval(
        id='interval-component',
        interval=1000,  
        n_intervals=0
    )
])

@app.callback(
    Output('live-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    try:
        if not os.path.exists(CSV_FILE):
            print("CSV not found!")
            return go.Figure()

        df = pd.read_csv(CSV_FILE)

        if df.empty or not all(col in df.columns for col in ['x', 'y', 'z']):
            print("Missing data columns")
            return go.Figure()

        df = df.tail(100)

        fig = go.Figure()
        fig.add_trace(go.Scatter(y=df['x'], mode='lines+markers', name='X-axis'))
        fig.add_trace(go.Scatter(y=df['y'], mode='lines+markers', name='Y-axis'))
        fig.add_trace(go.Scatter(y=df['z'], mode='lines+markers', name='Z-axis'))

        fig.update_layout(title='Live Accelerometer Data ',
                          xaxis_title='Sample',
                          yaxis_title='Acceleration',
                          legend_title='Axis',
                          template='plotly_dark')

        return fig

    except Exception as e:
        print(f"Callback error: {e}")
        return go.Figure()

if __name__ == '__main__':
    app.run(debug=True)  
