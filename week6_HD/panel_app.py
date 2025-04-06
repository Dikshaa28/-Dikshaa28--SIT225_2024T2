import pandas as pd
import panel as pn
import matplotlib.pyplot as plt

pn.extension('matplotlib')

# Load data
df = pd.read_csv('gyro_data.csv')

# Widgets
graph_type = pn.widgets.RadioButtonGroup(name='Graph Type', options=['Line', 'Scatter'], button_type='success')
axis_choice = pn.widgets.Select(name='Axis', options=['x', 'y', 'z', 'combined'])
num_points = pn.widgets.IntSlider(name='Number of Points', start=10, end=len(df), step=10, value=100)

# Plot function
@pn.depends(graph_type, axis_choice, num_points)
def plot_graph(g_type, axis, n_points):
    fig, ax = plt.subplots()
    data = df.head(n_points)
    timestamp = data['timestamp']

    if g_type == 'Line':
        if axis == 'combined':
            ax.plot(timestamp, data['x'], label='x', color='r')
            ax.plot(timestamp, data['y'], label='y', color='g')
            ax.plot(timestamp, data['z'], label='z', color='b')
        else:
            ax.plot(timestamp, data[axis], label=axis, color='m')
    else:
        if axis == 'combined':
            ax.scatter(timestamp, data['x'], label='x', color='r')
            ax.scatter(timestamp, data['y'], label='y', color='g')
            ax.scatter(timestamp, data['z'], label='z', color='b')
        else:
            ax.scatter(timestamp, data[axis], label=axis, color='m')

    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Axis Value')
    ax.set_title(f'{g_type} Plot - {axis.upper()} Axis')
    ax.legend()
    plt.tight_layout()
    return pn.pane.Matplotlib(fig, tight=True)

# Layout
dashboard = pn.Column(
    "# Gyroscope Data Visualization - Panel App 📈",
    graph_type,
    axis_choice,
    num_points,
    plot_graph
)

dashboard.servable()
