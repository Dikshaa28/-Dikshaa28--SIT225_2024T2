import pandas as pd
import os
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

file_path = "D:/python/week6/muski.csv"

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

    html.Div([
        html.Label("Select Chart Type:"),
        dcc.Dropdown(id="chart_type",
                     options=[{"label": c, "value": c} for c in ["Scatter", "Line", "Distribution"]],
                     value="Scatter"),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Select Variable (only for Distribution Plot):"),
        dcc.Dropdown(id="variable_select",
                     options=[{"label": var, "value": var} for var in ["x", "y", "z"]],
                     value="x"),
    ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),

    dcc.Graph(id="gyro_graph")
])

@app.callback(
    Output("gyro_graph", "figure"),
    Input("chart_type", "value"),
    Input("variable_select", "value")
)
def update_graph(chart_type, variable):
    if df.empty or "timestamp" not in df.columns:
        return px.scatter(title="No Data Available")

    if chart_type == "Scatter":
        fig = px.scatter(df, x="timestamp", y=["x", "y", "z"], title="Gyroscope Scatter Plot")
    elif chart_type == "Line":
        fig = px.line(df, x="timestamp", y=["x", "y", "z"], title="Gyroscope Line Chart")
    elif chart_type == "Distribution":
        if variable in df.columns:
            fig = px.histogram(df, x=variable, nbins=50, title=f"Distribution of {variable} values")
        else:
            fig = px.histogram(title="Invalid Variable Selected")
    else:
        fig = px.scatter(title="Unknown Chart Type")

    return fig

if __name__ == "__main__":
    app.run(debug=True)

