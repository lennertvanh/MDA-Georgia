import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__)

weather_data = pd.read_csv("Data for visualization/daily_weatherdata_2022.csv", header = 0, sep=',')

cutoff_rain_day = 0.0002

weather_data["bool_rainday"] = weather_data["LC_DAILYRAIN"] > cutoff_rain_day

rainy_counts = weather_data.groupby('Month')['bool_rainday'].sum()  # Count the number of rainy days per month

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# Create the bar chart
fig = go.Figure(data=go.Bar(x=months, y=rainy_counts))

# Set the color of bars to yellow
fig.update_traces(marker=dict(color='#E6AF2E'))
fig.update_traces(hovertemplate='%{x}: %{y}', hoverlabel=dict(namelength=0))

# Customize the chart layout
fig.update_layout(
    title=dict(text="Number of rainy days per month",x=0.5, font=dict(color="white")),
    xaxis_title="Month",
    yaxis_title="Number of rainy days", 
    title_font=dict(size=24),
    yaxis=dict(
        showgrid=True,
        zeroline=True,
        gridcolor='rgba(255, 255, 255, 0.1)',
        title_font=dict(color="white", size=18)
    ),
    xaxis=dict(
        showgrid=True,
        zeroline=True,
        gridcolor='rgba(255, 255, 255, 0.1)',
        title_font=dict(color="white", size=18)
    ),
    plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
    paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background color to transparent
)

fig.update_xaxes(color="white",gridwidth=5)
fig.update_yaxes(color="white")



layout = html.Div(children=[
    html.H1(children='Number of rainy days per month'),

    dcc.Graph(id="rain-graph", figure=fig),

])