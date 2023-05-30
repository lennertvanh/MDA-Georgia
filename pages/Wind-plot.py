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

data_weather = pd.read_csv("Data/daily_weatherdata_2022.csv")

avg_wind = data_weather.groupby("Month")["LC_WINDSPEED"].mean()

#############################################################################################
#figure 1

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
months_complete = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

###################################################################################################
#figure 2

#figure polar plot

base_direction = 135+90 #SW and correction polar plot having 0 on the right

data_weather["WINDDIR_transformed"]=data_weather["LC_WINDDIR"]

max_wind_avg = avg_wind.max()
avg_wind_rescaled = avg_wind/max_wind_avg


# Calculate weighted average wind direction for each month
monthly_avg_direction = data_weather.groupby(data_weather["Month"]) \
    .apply(lambda x: np.average(x["LC_WINDDIR"], weights=x["LC_WINDSPEED"])) \
    .reset_index(name="Weighted Avg Direction")

monthly_avg_direction["Weighted Avg Direction"] +=base_direction

#########################################################################################################
# Define app layout
layout = html.Div([
    html.Div([
        dcc.Graph(id='scatter-plot'),
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='wind-rose'),
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Br(),

    html.Div([
        dcc.Slider(
            id='month-slider',
            min=0,
            max=len(avg_wind) - 1,
            value=0,
            marks={i: {'label': months[i], 'style': {'font-weight': 'bold', 'font-size': '20px', 'color': 'white'}} for i in range(len(months))},
            step=None,
        )
    ],style={'width': '49%'},),
    
])

# Callback to update the wind rose graph based on the selected month
@callback(
    Output('wind-rose', 'figure'),
    [Input('month-slider', 'value')]
)
def update_wind_rose(selected_month):

    arrow_direction = monthly_avg_direction["Weighted Avg Direction"][selected_month]
    arrow_length = avg_wind_rescaled[selected_month+1]

    arrow_x = arrow_length * np.cos(np.deg2rad(arrow_direction))
    arrow_y = arrow_length * np.sin(np.deg2rad(arrow_direction))

    fig = go.Figure()

    # Add scatter plot points
    fig.add_trace(go.Scatterpolar(
        r=[0, arrow_length],  # Radius
        theta=[0, arrow_direction],  # Angle
        mode='lines',
        line=dict(
            color='#FC440F',
            width=3
        ),
    ))

    fig.add_trace(go.Scatterpolar(
        r=[arrow_length],
        theta=[arrow_direction],
        mode='markers',
        marker=dict(
            symbol="circle",  # Use a triangle marker to simulate an arrow#triangle-up
            size=12,
            color='#FC440F',
        ),
    ))

    # Set polar plot layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, 1]  # Set the range of the radial axis
            ),
            angularaxis=dict(
                visible=True,
                tickmode='array',
                tickvals=[0, 45, 90, 135, 180, 225, 270, 315],  # Set custom tick values for the angular axis
                ticktext=['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE'],  # Set custom tick labels for the angular axis
                tickfont=dict(color="white", size=18)
            )
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background color to transparent
        showlegend=False,
        title=dict(
        text='Dominant wind direction - ' + months_complete[selected_month] + ' 2022',
        x=0.5,  # Set the title's x position to center
        y=0.9,  # Set the title's y position to center
        xanchor='center',  # Set the x anchor to center
        yanchor='middle',  # Set the y anchor to middle
        font=dict(color="white", size=24)
        )   
    )

    fig.update_traces(hoverlabel=dict(namelength=0))
    fig.update_traces(hovertext=[''] * len(fig.data)) #remove the hovertext of r and theta, is not informative

    return fig

# Callback to update the scatter plot based on the selected month
@callback(
    [Output('scatter-plot', 'figure'),
    Output('scatter-plot', 'selectedData')],
    [Input('month-slider', 'value')]
)
def update_scatter_plot(selected_month):
    
    data = avg_wind[selected_month+1]
    avg_wind_speed_Uccle = [4.7, 4.5, 4.2, 3.5, 3.3, 3.1, 3.1, 3.1, 3.3, 3.8, 4.1, 4.6]

    fig = go.Figure()

    # Add the line shape 
    fig.add_shape(
        type='line',
        xref='x',
        yref='y',
        x0=months[selected_month],
        x1=months[selected_month],
        y0=0,
        y1=5,
        line=dict(
            color='rgba(255, 255, 255, 0.5)',  # white with opacity (0.5)
            width=2,
        )
    )

    # Add the average wind speed trace
    fig.add_trace(go.Scatter(
        x=months,
        y=avg_wind_speed_Uccle,
        mode='markers+lines',
        name='Average Wind Speed (Last 20 years)',
        marker=dict(color='#2A9D8F'),
        line=dict(color='#2A9D8F')
    ))

    # Add the red point trace
    fig.add_trace(go.Scatter(
        x=[months[selected_month], months[selected_month]],
        y=[data, avg_wind_speed_Uccle[selected_month]],
        mode='markers',
        marker=dict(
            color='#FC440F',
            size=15
        ),
        showlegend=False
    ))

    # Add the wind speed trace
    fig.add_trace(go.Scatter(
        x=months,
        y=avg_wind,
        mode='markers+lines',
        name='Wind Speed (2022)',
        marker=dict(color='#EB862E'),
        line=dict(color='#EB862E')
    ))

    # Set the layout
    fig.update_layout(
        title=dict(text='Wind Speed Comparison - Less wind in the city?', x=0.5, font=dict(color="white", size=24)),
        xaxis=dict(title='Month', showgrid=True, zeroline=True, gridcolor='rgba(255, 255, 255, 0.1)',
                title_font=dict(color="white", size=18)),
        yaxis=dict(title='Wind Speed (m/s)', showgrid=True, zeroline=True, gridcolor='rgba(255, 255, 255, 0.1)',
                title_font=dict(color="white", size=18)),
        plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background color to transparent
        hovermode='closest',
        legend=dict(orientation='h', y=1.1, yanchor='top'),
        shapes=[
            {
                'type': 'line',
                'xref': 'x',
                'yref': 'y',
                'x0': months[selected_month],
                'x1': months[selected_month],
                'y0': 0,
                'y1': 5,
                'line': dict(
                    color='rgba(255, 255, 255, 0.5)',  # white with opacity (0.5)
                    width=2,
                )
            }
        ]
    )


    fig.update_xaxes(color="white", gridwidth=2)
    fig.update_yaxes(color="white")
    fig.update_traces(hovertemplate='%{x}: %{y:.1f}m/s', hoverlabel=dict(namelength=0))

    # Text of the legend in white
    fig.update_layout(
        legend=dict(
            font=dict(color='white')
        )
    )

    return fig, None








