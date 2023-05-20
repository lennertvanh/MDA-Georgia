import dash
from dash import html, dcc, callback
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.graph_objects as go

dash.register_page(__name__)

#from kmi for Leuven from 1991 to 2020
#https://www.meteo.be/nl/klimaat/klimaat-van-belgie/klimaat-in-uw-gemeente
avg_rain_month = [70.4, 62.2, 54.4, 43.3, 55.5, 67.3, 72.7, 79.5, 60.5, 62.8, 68.5, 83.5 ]

weather_data = pd.read_csv("Data/daily_weatherdata_2022.csv")

weather_data["LC_DAILYRAIN_mm"] = weather_data["LC_DAILYRAIN"]*1000  #have in mm instead of m
total_rain_per_month = weather_data.groupby("Month")["LC_DAILYRAIN_mm"].sum()

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

#figure 1
# Create the scatter plots
fig1 = go.Figure()

# Add the scatter plot for average rainfall over the last 20 years
fig1.add_trace(go.Scatter(x=months, y=avg_rain_month, name="Average Rainfall (Last 20 Years)", mode="markers+lines"))

# Add the scatter plot for rainfall in 2022
fig1.add_trace(go.Scatter(x=months, y=total_rain_per_month, name="Rainfall in 2022", mode="markers+lines"))

# Update the layout
fig1.update_layout(
    title="Rainfall comparison between year 2022 and the average over the past 20 years",
    xaxis_title="Month",
    yaxis_title="Rainfall (mm)"
)


#figure 2

cutoff_rain_day = 0.0002

weather_data["bool_rainday"] = weather_data["LC_DAILYRAIN"] > cutoff_rain_day

rainy_counts = weather_data.groupby('Month')['bool_rainday'].sum()  # Count the number of rainy days per month


# Create the bar chart
fig2 = go.Figure(data=go.Bar(x=months, y=rainy_counts))

# Customize the chart layout
fig2.update_layout(
    title="Number of rainy days per month",
    xaxis_title="Month",
    yaxis_title="Number of rainy days"
)



layout = html.Div([
    html.H1("Rainfall Analysis"),
    dcc.Dropdown(
        id="figure-dropdown",
        options=[
            {"label": "Rainfall Comparison", "value": "figure1"},
            {"label": "Number of Rainy Days", "value": "figure2"}
        ],
        value="figure1"
    ),
    html.Div(id="figure-container")
])

@callback(
    Output("figure-container", "children"),
    [Input("figure-dropdown", "value")]
)
def update_figure(selected_figure):
    if selected_figure == "figure1":
        return dcc.Graph(figure=fig1)
    elif selected_figure == "figure2":
        return dcc.Graph(figure=fig2)