#########################################################################################################
# PACKAGES

import dash
from dash import html, dcc, callback
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import numpy as np

dash.register_page(__name__)

#########################################################################################################
# DATA

trafficimportances = pd.read_csv("Data for modelling/trafficimportances.csv", index_col=0)


heavydependence = pd.read_csv("Data for modelling/heavydependence.csv", index_col=0)
heavyvalues = pd.read_csv("Data for modelling/heavyvalues.csv", index_col=0)

cardependence = pd.read_csv("Data for modelling/cardependence.csv", index_col=0)
carvalues = pd.read_csv("Data for modelling/carvalues.csv", index_col=0)

bikedependence = pd.read_csv("Data for modelling/bikedependence.csv", index_col=0)
bikevalues = pd.read_csv("Data for modelling/bikevalues.csv", index_col=0)

peddependence = pd.read_csv("Data for modelling/peddependence.csv", index_col=0)
pedvalues = pd.read_csv("Data for modelling/pedvalues.csv", index_col=0)

#########################################################################################################
# VISUALIZATION

feature_names = ['heavy', 'car', 'bike', 'pedestrian']
importances = np.ravel(trafficimportances)

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=importances,
    y=feature_names,
    orientation='h',
    marker=dict(
        color="blue"
    )
))

fig1.update_layout(
    title='Traffic random forest permutation feature importance',
    xaxis_title='Mean MSE increase',
    yaxis_title='Feature',
    #width=400,  # Set the width of the plot to 800 pixels
    bargap=0.1,  # Set the gap between bars to 0.1 (adjust as needed)
    margin=dict(l=0, r=20, t=40, b=0)  # Set all margins to 0
)

#########################################################################################################
# PAGE LAYOUT

# Define the HTML page layout
layout = html.Div(
    children=[
        html.Div(
            [
                html.H2("Traffic model"),
                html.P("We scraped traffic data from Telraam, consisting of two weeks of complete observations between June 1 and June 14, measured between 3AM and 7PM. This is enough data for us to investigate how traffic variables impact the noise. A separate random forest was trained for this purpose, including the amount of heavy (heavier than a passenger vehicle), car, bicycle, and pedestrian traffic."),

            ]
        ),
html.Div(
                    children=[
                        dcc.Graph(
                            id='trafimp-plot-id',
                            figure=fig1,
                            style={'height': '100%', 'width': '600px'},
                        ),
                    ],
            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                ),
    ]
)

#########################################################################################################
# CALLBACK UPDATE FIGURE

# @callback(

# )
# def update_figure():
#    return None
