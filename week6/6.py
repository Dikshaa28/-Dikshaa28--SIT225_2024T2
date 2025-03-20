import pandas as pd
import os
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

file_path = "D:/python/week6/gyro_data.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)

    df.columns = df.columns.str.strip()

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
    else:
        print("Warning: 'timestamp' column not found!")

else:
    df = pd.DataFrame(columns=["timestamp", "x", "y", "z"])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Gyroscope Data Dashboard", style={'textAlign': 'center'}),

    dcc.Dropdown(id="chart_type",
                 options=[{"label": c, "value": c} for c in ["Scatter", "Line"]],
                 value="Scatter"),
    
    dcc.Graph(id="gyro_graph")
])

@app.callback(Output("gyro_graph", "figure"),
              Input("chart_type", "value"))
def update_graph(chart_type):
    if df.empty or "timestamp" not in df.columns:
        return px.scatter(title="No Data Available")

    if chart_type == "Scatter":
        fig = px.scatter(df, x="timestamp", y=["x", "y", "z"], title="Gyroscope Scatter Plot")
    else:
        fig = px.line(df, x="timestamp", y=["x", "y", "z"], title="Gyroscope Line Chart")

    return fig

if __name__ == "__main__":
    app.run(debug=True)
