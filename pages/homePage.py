import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

""" layout = html.Div(children=[
    #html.H1(children='Welcome to the home page of the app'),

    #html.Div(children='''
    #    Data about the city of Leuven will be analyzed and hopefully insight about it will be given.
    #'''),
    html.Div(
        style={'width': '400px', 'height': '400px', 'overflow': 'auto', 'border': '1px solid #000', 'padding': '10px'},
        children=[
            # Your content here
        ]
    )


]) """

import pandas as pd

weather_data = pd.read_csv("Data/daily_weatherdata_2022.csv", header = 0, sep=',')
cutoff_rain_day = 0.0002
weather_data["bool_rainday"] = weather_data["LC_DAILYRAIN"] > cutoff_rain_day
data_month = pd.read_csv('Data/monthly_weatherdata_2022.csv')


import plotly.graph_objects as go
import plotly.subplots as sp
import numpy as np

# Define the months and maximum days
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
max_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
"""
# Create an empty list to store the subplot figures
subplot_figures = []

# Iterate over each month
for month_num, month_name in enumerate(months):
    # Filter the weather data for the current month
    month_data = weather_data[weather_data["Month"] == month_num + 1]

    # Create an empty matrix to store the rain data
    matrix = np.zeros((1, max_days[month_num]))

    # Iterate over each day in the month
    for day in range(1, max_days[month_num] + 1):
        is_rainy = month_data[month_data["Day"] == day]["bool_rainday"].values[0]
        matrix[0, day - 1] = 1 if is_rainy else 0

    # Calculate the width and height of each cell in the heatmap
    cell_width = 1
    cell_height = 1 / len(matrix)

    color_zero = "red"
    color_one = "blue"

    #handle extreme cases where all dry or wet
    if np.all(matrix == 1):
        color_zero = "blue"
    elif np.all(matrix == 1):
        color_one = "red"

    # Create the heatmap figure
    fig = go.Figure(data=go.Heatmap(z=matrix, colorscale=[[0, color_zero], [1, color_one]],
                                   x=list(range(1, max_days[month_num] + 1)), y=[month_name],
                                   showscale=False, xgap=1, ygap=0.1))

    # Set the layout for the heatmap
    fig.update_layout(title="", #f"Rain in {month_name}",
                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=True),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=True,
                                 range=[-0.5, 0.5]),
                      height=50)

    # Append the subplot figure to the list
    subplot_figures.append(fig)

# Create a figure with subplots
fig = sp.make_subplots(rows=len(months), cols=1, shared_xaxes=True, vertical_spacing=0.05)   #, subplot_titles=months

# Add the heatmap subplots to the figure
for i, subplot_fig in enumerate(subplot_figures):
    fig.add_trace(subplot_fig.data[0], row=i + 1, col=1)

# Update the subplot layout
fig.update_layout(width=500,height=60 * len(months), title="Monthly Rain Heatmaps")
 """

import plotly.graph_objects as go
import numpy as np

# Filter the weather data for the month of January
january_data = weather_data[weather_data["Month"] == 1]

# Create an empty matrix to store the rain data
matrix = np.zeros((1, max_days[0]))

# Iterate over each day in January
for day in range(1, max_days[0] + 1):
    is_rainy = january_data[january_data["Day"] == day]["bool_rainday"].values[0]
    matrix[0, day - 1] = 1 if is_rainy else 0

# Calculate the width and height of each cell in the heatmap
cell_width = 1
cell_height = 10 / len(matrix)

# Create the heatmap figure
fig = go.Figure(data=go.Heatmap(z=matrix, colorscale=[[0, 'red'], [1, 'blue']],
                               x=list(range(1, max_days[0] + 1)),# y=["January"],
                               showscale=False,xgap=1))

# Set the layout for the heatmap
fig.update_layout(#title="Rain in January",
                  xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                  yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                             range=[-0.5,0.5]),
                  height=10,
                  margin=dict(l=0, r=0, t=0, b=0)  # Set the margins to 0 to remove padding
)

layout = html.Div(
    style={
        'display': 'flex',
        'justify-content': 'center',
        'height': '100vh',
    },
    children=[
        html.Div(
            style={'flex': '1'},
            children=[
                # Left div content here
            ]
        ),
        html.Div(
            style={'width': '520px', 'height': '250px', 'overflow': 'auto','overflow-x':'hidden', 'border': '1px solid #000', 'padding': '0px'},
            children=[
                
                
            ]
        ),
        html.Div(
            style={'flex': '1'},
            children=[
                # Right div content here
            ]
        ),
    ]
)

# Add 12 sub divs inside the central div
sub_divs = []

sub_div = html.Div(
        style={"position":"sticky",'width': '500px', 'height': '35px', 'border': '1px solid #000', 'margin': '0px','display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
        children=[
            html.Div(
                style={'width': '100px', 'height': '35px', 'border': '1px solid #000', 'margin': '0px','display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                children=[html.P("Month"),]),
            html.Div(
                style={'width': '50px', 'height': '35px', 'border': '1px solid #000', 'margin': '0px','display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                children=[html.P("Temp"),]),
            
            html.Div(
                style={'width': '300px','display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                children=[
                    html.P("Rainy days")
                ]
            ),

            html.Div(
                style={'width': '50px', 'height': '35px', 'border': '1px solid #000', 'margin': '0px','display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                children=[html.P("Wind"),]),
        ]
    )
sub_divs.append(sub_div)

for i in range(12):
    temp_avg_month = round(data_month[data_month['Month']==i+1]["LC_TEMP_QCL3"],1).values[0]
    wind_avg_month = round(data_month[data_month['Month']==i+1]["LC_WINDSPEED"],2).values[0]
    sub_div = html.Div(
        style={'width': '500px', 'height': '50px', 'border': '1px solid #000', 'margin': '0px','display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
        children=[
            html.Div(
                style={'width': '100px', 'height': '50px', 'border': '1px solid #000', 'margin': '0px','display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                children=[html.P(f"{months[i]}"),]),
            html.Div(
                style={'width': '50px', 'height': '50px', 'border': '1px solid #000', 'margin': '0px','display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                children=[html.P(f"{temp_avg_month}"),]),
            
            html.Div(
                style={'width': '300px'},
                children=[
                    dcc.Graph(figure=fig, style={'max-width': '100%'})
                ]
            ),

            html.Div(
                style={'width': '50px', 'height': '50px', 'border': '1px solid #000', 'margin': '0px','display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                children=[html.P(f'{wind_avg_month}'),]),
        ]
    )
    sub_divs.append(sub_div)

layout.children[1].children += sub_divs
