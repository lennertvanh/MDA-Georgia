import plotly.graph_objects as go
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

dash.register_page(__name__)


# Load the data
data_noise = pd.read_csv('Data for visualization/combined_noise_event.csv', header=0, sep=',')

# Calculate the frequencies of each category in the 'noise_source' variable
category_counts = data_noise['noise_event_laeq_primary_detected_class'].value_counts()

# Sort the categories by frequency in descending order
sorted_categories = category_counts.index.tolist()

# Calculate the total number of categories
num_categories = len(category_counts)

# Calculate the opacity levels
opacity_levels = [i / (num_categories - 1) for i in range(num_categories)]

# Reverse the list to make the largest category have the strongest opacity
opacity_levels.reverse()  

# Create a list of colors with adjusted opacity
colors = [f"rgba(227, 74, 111, {opacity})" for opacity in opacity_levels]

# Create a donut plot with customized colors
fig = go.Figure(data=[
    go.Pie(
        labels=category_counts.index,
        values=category_counts.values,
        hole=0.6,
        marker=dict(colors=colors),
        textfont=dict(color='white'),
        showlegend=False,
        hovertemplate='<b>Noise source</b>: %{label}<br>'
                      '<b>Count</b>: %{value}<br>'
                      '<b>Percentage</b>: %{percent:.1%}<extra></extra>'
    )
])

# Set the layout options for the donut plot
fig.update_layout(
    title=go.layout.Title(
        text="Noise Events <br>Distribution",
        x=0.5,
        y=0.45,
        xanchor="center",
        yanchor="middle",
        font=dict(color="white") 
    ),
    showlegend=False,
    legend_title="Noise Sources",
    width=400,
    height=400,
    margin=go.layout.Margin(
        l=20,
        r=20,
        b=20,
        t=80,
        pad=4
    ),
    plot_bgcolor="white",
    paper_bgcolor="rgba(0,0,0,0)"
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
    line_color="rgba(0,0,0,0)",
    fillcolor="rgba(0,0,0,0)",
)

# Define the app layout
layout = html.Div([
    dcc.Graph(id='donut-chart', figure=fig)
])
