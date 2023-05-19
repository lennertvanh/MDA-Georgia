import dash
from dash import dcc, html, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

dash.register_page(__name__)

# Loading noise data
data_noise = pd.read_csv('../Data/combined_noisedata_2022.csv', header=0, sep=',', parse_dates=["result_date"])
data_noise.head()

# Line chart visualization 
fig = px.line(data_noise, x="result_date", y="laeq", title="Laeq Over Time")

# Defining the app layout 
layout = html.Div(
    children=[
        html.H1("Noise Level Analysis"),
        dcc.Graph(id="noise-graph", figure=fig),
        dcc.RangeSlider(
            id="date-slider",
            marks={i: pd.Timestamp(year=2022, month=i, day=1).strftime("%B") for i in range(1, 13)},
            min=1,
            max=12,
            value=[1, 12],
            step=1,
        ),
    ]
)

@callback(
    dash.dependencies.Output("noise-graph", "figure"),
    [dash.dependencies.Input("date-slider", "value")]
)
def update_graph(date_range):
    start_month, end_month = date_range
    filtered_data = data_noise[
        (data_noise["result_date"].dt.month >= start_month) &
        (data_noise["result_date"].dt.month <= end_month)
    ]
    fig = px.line(filtered_data, x="result_date", y="laeq", title="Noise Levels Over Time")
    return fig
