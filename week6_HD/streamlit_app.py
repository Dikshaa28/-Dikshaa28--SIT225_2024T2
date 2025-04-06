import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV
df = pd.read_csv("gyro_data.csv")  # make sure this file exists in your folder

# Sidebar controls
st.sidebar.title("Dashboard Controls")
axes = st.sidebar.multiselect("Select Axes", ["x", "y", "z"], default=["x", "y", "z"])
graph_type = st.sidebar.radio("Graph Type", ["Line", "Scatter"])
sample_range = st.sidebar.slider("Sample Range", 0, len(df), (0, 300))

# Subset the data
subset = df.iloc[sample_range[0]:sample_range[1]]

# Title
st.title("Gyroscope Data Dashboard")

# Plot
st.subheader(f"{graph_type} Plot")
fig, ax = plt.subplots()
for axis in axes:
    if graph_type == "Line":
        ax.plot(subset[axis], label=axis)
    else:
        ax.scatter(range(len(subset)), subset[axis], label=axis, s=10)

ax.legend()
ax.set_xlabel("Sample")
ax.set_ylabel("Gyro Value")
st.pyplot(fig)

# Summary Table
st.subheader("Data Summary")
st.dataframe(subset[axes].describe())



# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# # fake gyro data instead of reading a CSV
# data = {
#     'x': [0.1, 0.5, 0.2, 0.7, 0.3],
#     'y': [0.2, 0.4, 0.1, 0.9, 0.3],
#     'z': [0.3, 0.6, 0.2, 0.8, 0.5]
# }
# df = pd.DataFrame(data)

# st.title("📊 Simple Streamlit Dashboard")
# st.write("This is a sample gyroscope data dashboard.")

# # Show raw data
# st.dataframe(df)

# # Plotting graph
# st.line_chart(df)
