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

layout = html.Div(
    children=[
        html.H2("What are the noisiest months in Leuven?", style={'margin-bottom': '20px'}),
        html.P("To discover which months of 2022 were on average the loudest, we can take a look at the average noise level for each month. Since the differences between the months are quite small, we added the option to look at the standardized average noise levels. This allows us to compare them more precisely. What becomes clear is that the noise in Leuven is likely determined by the students. Months where students start a new semester (February, March, October, November) are the loudest in Leuven, with many student activities happening around the centre. In the months right before and during exam season (January, May, June, August, December), on the other hand, Leuven becomes a bit more quiet. The quietest time, however, is during summer vacation (July), since many students leave the city to return home or leave on holiday."),
        dcc.Graph(id="noise-per-month-graph"),
        dcc.RadioItems(
            id='data-type-radio',
            options=[
                {'label': 'Figure Absolute Values', 'value': 'absolute'},
                {'label': 'Figure Standardized Values', 'value': 'standardized'}
            ],
            value='standardized',
            labelStyle={'display': 'inline-block'},
            style={'margin-left': '20px', 'margin-bottom': '20px', 'margin-top': '20px'}
        ),
    ]
)


@callback(
    Output("noise-per-month-graph", "figure"),
    [Input("data-type-radio", "value")]
)

def update_graph(data_type):
    if data_type == 'standardized':
        fig = go.Figure(data=go.Bar(x=months, y=average_noise_std))
        fig.update_traces(marker=dict(color=['#FEFE62' if val < 0 else '#D35FB7' for val in average_noise_std]))
        fig.update_layout(
            title=dict(text="Average noise level per month (standardized data)",x=0.5, font=dict(
            color="white")),
            xaxis_title="Month",
            yaxis_title="Average noise level (Laeq)", plot_bgcolor='#2E2E3A', paper_bgcolor='#2E2E3A', title_font=dict(size=30), xaxis=dict(showgrid=True, zeroline=True),
                            yaxis=dict(showgrid=True, zeroline=True)
        )
        fig.update_xaxes(color="white",gridwidth=5)
        fig.update_yaxes(color="white")
    else:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=months, y=average_noise, showlegend=False))
        fig.add_trace(go.Scatter(
            x=[months[0], months[-1]],
            y=[average_noise.mean()] * 2,
            mode='lines',
            line=dict(color='#009a9c', width=3),
            name='Average Line',
            showlegend=True
        ))
        fig.update_traces(marker=dict(color=['#FEFE62' if val < 0 else '#D35FB7' for val in average_noise_std]))
        fig.update_layout(
            title=dict(text="Average noise level per month (absolute value of the data)",x=0.5, font=dict(
            color="white")),
            xaxis_title="Month",
            yaxis_title="Average noise level (Laeq)", 
            plot_bgcolor='#2E2E3A',
            paper_bgcolor='#2E2E3A',
            title_font=dict(size=30),
            yaxis=dict(showgrid=True, zeroline=True),
            xaxis=dict(showgrid=True, zeroline=True),
            legend=dict(
                title="Legend",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        fig.update_xaxes(color="white",gridwidth=5)
        fig.update_yaxes(color="white")
    
    return fig
