import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Select
from bokeh.layouts import column

# Load data
df = pd.read_csv("gyro_data.csv")

# UI Controls
graph_type_select = Select(title="Graph Type", value="Line", options=["Line", "Scatter"])
axis_select = Select(title="Axis", value="X", options=["X", "Y", "Z", "XYZ"])
points_select = Select(title="Number of Points", value="100", options=["100", "500", "1000", "All"])

# Plot and source
source = ColumnDataSource(data=dict(x=[], y=[]))
plot = figure(title="", x_axis_label="Timestamp", y_axis_label="Value", height=400, width=700)
renderer = plot.line('x', 'y', source=source)  # Default renderer (line)

# Update function
def update_plot(attr, old, new):
    n = len(df) if points_select.value == "All" else int(points_select.value)
    d = df.head(n)
    axis = axis_select.value
    gtype = graph_type_select.value

    plot.renderers.clear()
    
    if axis == "XYZ":
        colors = {'x': 'red', 'y': 'green', 'z': 'blue'}
        for a in ['x', 'y', 'z']:
            s = ColumnDataSource(data={'x': d['timestamp'], 'y': d[a]})
            if gtype == "Line":
                plot.line('x', 'y', source=s, legend_label=a.upper(), line_color=colors[a])
            else:
                plot.circle('x', 'y', source=s, legend_label=a.upper(), color=colors[a], size=5)
    else:
        axis_col = axis.lower()
        source.data = {'x': d['timestamp'], 'y': d[axis_col]}
        if gtype == "Line":
            renderer = plot.line('x', 'y', source=source, line_width=2)
        else:
            renderer = plot.circle('x', 'y', source=source, size=6)

    plot.legend.visible = axis == "XYZ"

# Callbacks
for control in [graph_type_select, axis_select, points_select]:
    control.on_change("value", update_plot)

update_plot(None, None, None)

# Layout
layout = column(graph_type_select, axis_select, points_select, plot)
curdoc().add_root(layout)
