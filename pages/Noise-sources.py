import plotly.graph_objects as go
import pandas as pd
import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import plotly.colors

dash.register_page(__name__)


# Load the data
data_noise = pd.read_csv('Data for visualization/combined_noise_event.csv', header=0, sep=',')

# Calculate the frequencies of each category in the 'noise_source' variable
category_counts = data_noise['noise_event_laeq_primary_detected_class'].value_counts()

# Sort the categories by frequency in descending order
sorted_categories = category_counts.index.tolist()

# Define the colorscale for the chart
colorscale = plotly.colors.sequential.Redor_r

# Adjust the colorscale to have seven shades
colorscale = colorscale[:7]

# Create a dictionary to map each category to its corresponding color
category_colors = {category: color for category, color in zip(sorted_categories, colorscale)}

# Create a list of colors for each category based on the frequencies
colors = [category_colors[category] for category in category_counts.index]

# Create a donut plot with customized colors
fig = go.Figure(data=[
    go.Pie(
        labels=category_counts.index,
        values=category_counts.values,
        hole=0.6,
        marker=dict(colors=colors)
    )
])

# Set the layout options for the donut plot
fig.update_layout(
    title="Distribution of Noise Sources",
    showlegend=True,
    legend_title="Noise Sources",
    width=600,
    height=600
)

# Add a white circle to create the donut effect
fig.add_shape(
    type="circle",
    xref="paper",
    yref="paper",
    x0=0.35,
    y0=0.35,
    x1=0.65,
    y1=0.65,
    line_color="white",
    fillcolor="white"
)


# Define the app layout
layout = html.Div([
    dcc.Graph(id='donut-chart', figure=fig)
])
