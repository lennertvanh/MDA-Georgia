#########################################################################################################
# PACKAGES

import dash
from dash import dcc, html, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.colors
from datetime import datetime

dash.register_page(__name__)

#########################################################################################################
# DATA

# Loading noise data
data_noise = pd.read_csv('Data for visualization/daily_noisedata_2022.csv', header=0, sep=',')

# Only keeping the observations for Naamsestraat 62 - Taste since this is the only location with observations for each month
value_to_keep = 'MP 03: Naamsestraat 62 Taste'
data_noise = data_noise[data_noise['description'] == value_to_keep]

# Changing format of 'date' variable
data_noise['date'] = pd.to_datetime(data_noise['date'], format='%d-%m-%Y')

# Sort the data by 'date' column
data_noise = data_noise.sort_values('date')

# Loading holiday data
holiday_data = pd.read_csv('Data for visualization/Holiday_dummies.csv')
holiday_data['index'] = pd.to_datetime(holiday_data['index'])

# Format 'index' column to the desired format "01-01-2022"
holiday_data['index'] = holiday_data['index'].dt.strftime("%Y-%m-%d")
holiday_data.head(30)

# Drop duplicates based on 'index' in the 'data' dataset
holiday_data = holiday_data.drop_duplicates(subset='index')
holiday_data.head(10)

holiday_data['index'] = pd.to_datetime(holiday_data['index'])
data_noise = pd.merge(holiday_data,data_noise, left_on='index', right_on='date', how='inner')

#days per month
month_days = [31,28,31,30,31,30,31,31,30,31,30,31]

#########################################################################################################
# VISUALIZATION

# Create line chart
fig = px.line(data_noise, x="date", y="laeq", title="Noise levels over time")

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', 
    paper_bgcolor='rgba(0,0,0,0)',  
    title=dict(
        text="Average noise levels over time - Taste (Naamsestraat 62)",
        font=dict(color="white"),
        
    ),
    title_font=dict(size=24),
    xaxis=dict(
        title="Date",
        title_font=dict(color="white", size =18),
        tickfont=dict(color="white"),
        gridcolor='rgba(255, 255, 255, 0.1)',
        tickmode='linear', 
        dtick='M1'
    ),
    yaxis=dict(
        title="Noise level (dB(A))",
        title_font=dict(color="white", size = 18),
        tickfont=dict(color="white"),
        gridcolor='rgba(255, 255, 255, 0.1)'
    ),
    margin=dict(l=50, r=50, t=50, b=50),
    hoverlabel=dict(namelength=0),
    legend=dict(
        font=dict(
            color='white'
        )
    )  
)

# Change the line color
fig.update_traces(line=dict(color='#E6AF2E', width=3))

# Add red markers for holidays
holiday_dates = data_noise[data_noise['Holiday'] == 1]['date']
holiday_laeq = data_noise[data_noise['Holiday'] == 1]['laeq']

fig.add_trace(go.Scatter(
    x=holiday_dates,
    y=holiday_laeq,
    mode='markers',
    marker=dict(color='#F62DAE', symbol='circle', size=8),
    name='Holiday',
    showlegend=True,
    hovertemplate='Date: %{x}<br>Noise Level: %{y:.2f} dB(A)',
    hoverlabel=dict(namelength=0)
))



#########################################################################################################
# PAGE LAYOUT

# Define page layout
layout = html.Div(
    children=[
        html.H2("Exploring the dynamic patterns of city noise in Leuven"),  
        html.P("The best way to get a first look at the monitored noise levels is to plot them over time. Holidays mostly appear to be either situated in peaks or valleys of the time series."), 
        html.Div(
            className="plot-container",  
            style={'padding': '20px', 'max-width': '90vw', 'justify-content': 'center'},
            children=[
                dcc.Graph(id="noise-graph", figure=fig, className="plot-container"),
                dcc.RangeSlider(
                    id="date-slider",
                    marks={i: {'label': pd.Timestamp(year=2022, month=i, day=1).strftime("%B"), 'style': {'font-weight': 'bold', 'color': 'white'}} for i in range(1, 13)},
                    min=1,
                    max=12,
                    value=[1, 12],
                    step=1,
                ),
                dcc.Checklist(
                    id='average-checkbox',
                    options=[
                        {'label': 'Show Yearly Average', 'value': 'average'},
                        {'label': 'Show Monthly Average', 'value': 'monthly'}
                    ],
                    value=[]
                )
            ]
        )
    ]
)

#########################################################################################################
# CALLBACK UPDATE GRAPH

# Callback
@callback(
    Output("noise-graph", "figure"),
    [Input("date-slider", "value"), Input("average-checkbox", "value")],  
)
def update_graph(date_range, show_average):
    start_month, end_month = date_range

    
    
    # Filter the data based on the selected date range
    filtered_data = data_noise[
        (data_noise["date"].dt.month >= start_month) &
        (data_noise["date"].dt.month <= end_month)
    ]
    # Update x and y values for the line chart
    x = filtered_data["date"]
    y = filtered_data["laeq"]


    # Create a new figure object
    fig = go.Figure()
    
    # Add the line trace to the figure
    fig.add_trace(go.Scatter(
        x=filtered_data["date"],
        y=filtered_data["laeq"],
        mode="lines",
        name="Noise levels over time",
        line=dict(color='#E6AF2E', width=4),
        hoverlabel=dict(namelength=0),
        hovertemplate='Date: %{x}<br>Noise Level: %{y:.2f} dB(A)'
    ))
    
    fig.add_trace(go.Scatter(
        x=holiday_dates,
        y=holiday_laeq,
        mode='markers',
        marker=dict(color='#F62DAE', symbol='circle', size=8),
        name='Holiday',
        showlegend=True,
        hovertemplate='Date: %{x}<br>Noise Level: %{y:.2f} dB(A)',
        hoverlabel=dict(namelength=0)
    ))
    
    if "average" in show_average:
        # Calculate overall yearly average Laeq
        overall_average = data_noise["laeq"].mean()
        
        # Create a line trace for the overall yearly average
        fig.add_trace(go.Scatter(
            x=[filtered_data["date"].min(), filtered_data["date"].max()],
            y=[overall_average, overall_average],
            mode="lines",
            name="Yearly Average",
            line=dict(color="red"),
            showlegend=False,
            hoverlabel=dict(namelength=0),
            hovertemplate="Yearly Average:<br>%{y:.2f} dB(A)"
        ))
   
            
    if "monthly" in show_average:
        # Calculate monthly average Laeq for each month
        monthly_average = filtered_data.groupby(filtered_data["date"].dt.month)["laeq"].mean()
        
        # Create a line trace for each month's average
        for month, average in monthly_average.items():
            # Filter the data to include only the corresponding month
            month_data = filtered_data[filtered_data["date"].dt.month == month]
            
            fig.add_trace(go.Scatter(
                x=month_data["date"],
                y=[average] * len(month_data),
                mode="lines",
                name=f"Monthly Average - {pd.Timestamp(month=month, year=2022, day=1).strftime('%B')}",
                line=dict(color="#2A9D8F"),
                showlegend=False,
                hoverlabel=dict(namelength=0),
                hovertemplate=f"Monthly Average - {pd.Timestamp(month=month, year=2022, day=1).strftime('%B')}:<br>{average:.2f} dB(A)" #instead of y
            ))
    
    # Update layout of the figure
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title=dict(
            text="Average noise levels over time - Taste (Naamsestraat 62)",
            font=dict(color="white")
        ),
        title_font=dict(size=24),
        xaxis=dict(
            title="Date",
            title_font=dict(color="white", size=18),
            tickfont=dict(color="white"),
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickmode='linear',
            dtick='M1'
        ),
        yaxis=dict(
            title="Noise level (dB(A))",
            title_font=dict(color="white", size=18),
            tickfont=dict(color="white"),
            gridcolor='rgba(255, 255, 255, 0.1)'
        ),
        margin=dict(l=50, r=50, t=50, b=50),
        hoverlabel=dict(namelength=0),
        legend=dict(
        font=dict(
            color='white'
        )
    )  
    )
    
    # Set the x-axis range based on the selected date range
    fig.update_xaxes(range=[
        pd.Timestamp(year=2022, month=start_month, day=1),
        pd.Timestamp(year=2022, month=end_month, day=month_days[end_month-1])
    ])

    
    return fig