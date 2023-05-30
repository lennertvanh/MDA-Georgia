#########################################################################################################
# PACKAGES

import plotly.graph_objects as go
import pandas as pd
import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output

dash.register_page(__name__)

#########################################################################################################
# DATA

# Loading noise and weather data
weather_data = pd.read_csv("Data for visualization/daily_weatherdata_2022.csv", header = 0, sep=',')
data_noise = pd.read_csv('Data for visualization/daily_noisedata_2022.csv', header=0, sep=',', parse_dates=["date"])

# Define cutoff value for rainy day
cutoff_rain_day = 0.002
weather_data["bool_rainday"] = weather_data["LC_DAILYRAIN"] > cutoff_rain_day

# Standardized values
average_noise = data_noise.groupby('month')['laeq'].mean()

mean_average_noise = average_noise.mean()
std_average_noise = average_noise.std()

average_noise_std = (average_noise-mean_average_noise)/std_average_noise

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# Calculate the maximum value of average_noise_std
max_value = max(average_noise_std)

# Set the desired color and opacity values
color = '#E6AF2E'  
opacity = [0.5 if val < max_value else 1.0 for val in average_noise_std]  


#########################################################################################################
# PAGE LAYOUT

layout = html.Div(
    children=[
        html.H2("What are the noisiest months in Leuven?", style={'margin-bottom': '20px'}),
        html.P("To discover which months of 2022 were on average the loudest, we can take a look at the average noise level for each month. Since the differences between the months are quite small, we added the option to look at the standardized average noise levels. This allows us to compare them more precisely. What becomes clear is that the noise in Leuven is likely determined by the students. Months where students start a new semester (February, March, October, November) are the loudest in Leuven, with many student activities happening around the centre. In the months right before and during exam season (January, May, June, August, December), on the other hand, Leuven becomes a bit more quiet. The quietest time, however, is during summer vacation (July), since many students leave the city to return home or leave on holiday."),
        html.Div(
            className="plot-container",  
            style={'padding': '20px', 'max-width': '90vw', 'justify-content': 'center'},
            children=[
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
                )
            ]
        )
    ]
)

#########################################################################################################
# CALLBACK UPDATE GRAPH

@callback(
    Output("noise-per-month-graph", "figure"),
    [Input("data-type-radio", "value")]
)

def update_graph(data_type):
    if data_type == 'standardized':
        fig = go.Figure(data=go.Bar(x=months, y=average_noise_std))
        fig.update_traces(marker=dict(color=['#2A9D8F' if val < 0 else '#EB862E' for val in average_noise_std]))
        fig.update_layout(
            title=dict(text="Average noise level per month (standardized values)", font=dict(
            color="white", size=24)),
            xaxis_title="Month",
            yaxis_title="Average noise level<br> (Laeq in dB(A))", title_font=dict(size=24), xaxis=dict(title_font=dict(color="white", size =18),showgrid=True, zeroline=True,  gridcolor='rgba(255, 255, 255, 0.1)'),
            yaxis=dict(title_font=dict(color="white", size =18),showgrid=True, zeroline=True,  gridcolor='rgba(255, 255, 255, 0.1)'),
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            
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
            line=dict(color='#e9ff70', width=3),
            name='Average Line',
            showlegend=True
        ))
        fig.update_traces(marker=dict(color=color, opacity=opacity))
        fig.update_layout(
            title=dict(text="Average noise level per month (absolute values)",font=dict(
            color="white")),
            xaxis_title="Month",
            yaxis_title="Average noise level (dB(A))", 
            title_font=dict(size=24),
            yaxis=dict(showgrid=True, zeroline=True, gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),),
            xaxis=dict(showgrid=True, zeroline=True,  gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),),
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                title="Legend",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='white')
                 
            )
        )
        fig.update_xaxes(color="white",gridwidth=5)
        fig.update_yaxes(color="white")
    
    return fig
