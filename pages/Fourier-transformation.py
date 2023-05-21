import dash
from dash import html, dcc, callback
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

dash.register_page(__name__)

#intercept always added
labels = ["day-night","12 hours","day","half-week","week","month","season","half year"]
labels_complete = ["intercept","day","month","season","day-night","week","half-week","12 hours","half year"]

x = [1, 2, 3, 4, 5]
y = [10, 5, 7, 8, 3]
fig1 = go.Figure(data=go.Scatter(x=x, y=y, mode='markers'))

# Define the HTML layout
layout = html.Div(
    style={'display': 'flex', 'height': '50vh'},
    children=[
        html.Div(
            style={'width': '15%'},
            children=[
                html.Div('Left Content')
            ]
        ),
        html.Div(
            style={'width': '70%', 'position': 'relative'},
            children=[
                dcc.Graph(id='graph-Fourier', figure=fig1)
                   
            ]
        ),
        html.Div(
            style={'width': '15%', 'position': 'relative'},
            children=[
                html.Div(
                    children=[
                        dcc.Checklist(
                            id='checklist',
                            options=[{'label': label, 'value': label} for label in labels],
                            value=[], 
                            style={'margin-bottom': '5px','display':'block'},
                            labelStyle={'display':'block'}
                        )
                    ]
                )
            ]
        )
    ]
)



data_noise = pd.read_csv("Data/combined_noisedata_2022.csv")

@callback(
    Output('graph-Fourier', 'figure'),
    [Input('checklist', 'value')],
    suppress_callback_exceptions=True #in the app?
)
def update_figure(selected_values):
    # Create a new figure based on the selected values
    # Perform your desired logic here to update the figure
    # Example: Updating the y-values based on the selected values

    # Filter the data based on the selected values
    #filtered_y = [y[i-1] for i in selected_values]  # Assuming selected_values are 1-indexed

    print(selected_values)
    # Create a new scatter plot figure
    #new_figure = go.Figure(data=go.Scatter(x=x, y=filtered_y, mode='markers'))
    selected_values = selected_values

    x = [1, 2, 3, 4, 5]
    y = [3, 7, 7, 2, 3]
    new_figure = go.Figure(data=go.Scatter(x=x, y=y, mode='markers'))

    return new_figure 
