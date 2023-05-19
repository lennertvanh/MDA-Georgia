import plotly.graph_objects as go
import pandas as pd
import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output

dash.register_page(__name__)

weather_data = pd.read_csv("Data/daily_weatherdata_2022.csv", header = 0, sep=',')
weather_data.head()

cutoff_rain_day = 0.002

weather_data["bool_rainday"] = weather_data["LC_DAILYRAIN"] > cutoff_rain_day



data_noise = pd.read_csv('Data/combined_noisedata_2022.csv', header=0, sep=',', parse_dates=["result_date"])
data_noise.head()


#standardized values
average_noise = data_noise.groupby('result_month')['laeq'].mean()

mean_average_noise = average_noise.mean()
std_average_noise = average_noise.std()

average_noise_std = (average_noise-mean_average_noise)/std_average_noise

import plotly.graph_objects as go

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

""" fig = go.Figure(data=go.Bar(x=months, y=average_noise_std))

# Set the color of bars based on the value
fig.update_traces(marker=dict(color=['red' if val < 0 else 'green' for val in average_noise_std]))

fig.update_layout(
    title="Average noise level per month (standardized data)",
    xaxis_title="Month",
    yaxis_title="Average noise level (Laeq)"
) """



""" #absolute values
fig2 = go.Figure()

# Add the bar trace with showlegend=False
fig2.add_trace(go.Bar(x=months, y=average_noise, showlegend=False))

# Add the black line for the average with showlegend=True
fig2.add_trace(go.Scatter(x=[months[0], months[-1]], y=[average_noise.mean()] * 2, mode='lines',
                         line=dict(color='black', width=2), name='Average Line', showlegend=True))

fig2.update_traces(marker=dict(color=['red' if val < 0 else 'green' for val in average_noise_std]))

fig2.update_layout(
    title="Average noise level per month (absolute value of the data)",
    xaxis_title="Month",
    yaxis_title="Average noise level (Laeq)",
    legend=dict(
        title="Legend",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)"""


#layout = html.Div(children=[
#   html.H1(children='Noise per month'),
#
#    dcc.Graph(id="noise-per-month-graph", figure=fig),

#])

layout = html.Div(children=[
    html.H1(children='Noise per month'),
    
    dcc.RadioItems(
        id='data-type-radio',
        options=[
            {'label': 'Figure Absolute Values', 'value': 'absolute'},
            {'label': 'Figure Standardized Values', 'value': 'standardized'}
        ],
        value='standardized',
        labelStyle={'display': 'inline-block'}
    ),
    
    dcc.Graph(id="noise-per-month-graph")
])

@callback(
    Output("noise-per-month-graph", "figure"),
    [Input("data-type-radio", "value")]
)

def update_graph(data_type):
    if data_type == 'standardized':
        fig = go.Figure(data=go.Bar(x=months, y=average_noise_std))
        fig.update_traces(marker=dict(color=['red' if val < 0 else 'green' for val in average_noise_std]))
        fig.update_layout(
            title="Average noise level per month (standardized data)",
            xaxis_title="Month",
            yaxis_title="Average noise level (Laeq)"
        )
    else:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=months, y=average_noise, showlegend=False))
        fig.add_trace(go.Scatter(
            x=[months[0], months[-1]],
            y=[average_noise.mean()] * 2,
            mode='lines',
            line=dict(color='black', width=2),
            name='Average Line',
            showlegend=True
        ))
        fig.update_traces(marker=dict(color=['red' if val < 0 else 'green' for val in average_noise_std]))
        fig.update_layout(
            title="Average noise level per month (absolute value of the data)",
            xaxis_title="Month",
            yaxis_title="Average noise level (Laeq)",
            legend=dict(
                title="Legend",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
    
    return fig
