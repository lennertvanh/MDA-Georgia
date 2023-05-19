import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__)

weather_data = pd.read_csv("Data/daily_weatherdata_2022.csv", header = 0, sep=',')

cutoff_rain_day = 0.002

weather_data["bool_rainday"] = weather_data["LC_DAILYRAIN"] > cutoff_rain_day

rainy_counts = weather_data.groupby('Month')['bool_rainday'].sum()  # Count the number of rainy days per month

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# Create the bar chart
fig = go.Figure(data=go.Bar(x=months, y=rainy_counts))

# Customize the chart layout
fig.update_layout(
    title="Number of rainy days per month",
    xaxis_title="Month",
    yaxis_title="Number of rainy days"
)



layout = html.Div(children=[
    html.H1(children='Number of rainy days per month'),

    dcc.Graph(id="rain-graph", figure=fig),

])