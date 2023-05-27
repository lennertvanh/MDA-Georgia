import dash
from dash import dcc, html, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.colors

dash.register_page(__name__)

# Loading noise data
data_noise = pd.read_csv('Data/daily_noisedata_2022.csv', header=0, sep=',')
#data_holidays = pd.read_csv('Data/Holiday_dummies.csv', header=0, sep=',')

# Create datetime variable for holiday data
#data_holidays['result_date'] = pd.to_datetime(data_holidays['index']).dt.date

# Only keeping the observations for Naamsestraat 62 - Taste since this is the only location with observations for each month
value_to_keep = 'MP 03: Naamsestraat 62 Taste'

# Boolean indexing to filter the DataFrame
data_noise = data_noise[data_noise['description'] == value_to_keep]

# Create new column 'year'
data_noise['year'] = 2022

# Combine 'hour', 'day', 'month', and 'year' columns to create a new 'result_date' column
data_noise['result_date'] = pd.to_datetime(data_noise[['year', 'month', 'day']])

# Sort the DataFrame by 'result_date' column
data_noise = data_noise.sort_values('result_date')

# Merge the two datasets
#data_holidays = data_holidays.drop_duplicates(subset='result_date') # dropping duplicates
#data_noise = pd.concat([data_noise, data_holidays.set_index('result_date')], axis=1, join='inner').reset_index()

# Line chart visualization
fig = px.line(data_noise, x="result_date", y="laeq", title="Noise levels over time")

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
    paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background color to transparent
    title=dict(
        text="Noise levels over time",
        font=dict(color="white")
    ),
    xaxis=dict(
        title="Result Date",
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    ),
    yaxis=dict(
        title="Laeq",
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    ),
    margin=dict(l=100, r=100, t=50, b=50)
)

# Change the line color
fig.update_traces(line=dict(color='#E6AF2E', width=3))

# Defining the app layout
layout = html.Div(
    children=[
        html.H2("Exploring the dynamic patterns of city noise in Leuven"),  # Title outside the frame
        html.P("The best way to get a first look at the monitored noise levels is to plot them over time. (add some extra text) "),  # Paragraph outside the frame
        html.Div(
            className="plot-container",  # Add the CSS class to this div element
            style={'padding': '20px', 'max-width': '90vw', 'justify-content': 'center'},
            children=[
                dcc.Graph(id="noise-graph", figure=fig,  className="plot-container"),
                dcc.RangeSlider(
                    id="date-slider",
                    marks={i: pd.Timestamp(year=2022, month=i, day=1).strftime("%B") for i in range(1, 13)},
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

@callback(
        Output("noise-graph", "figure"),
    [Input("date-slider", "value"), Input("average-checkbox", "value"), Input("noise-graph", "figure")],
)

def update_graph(date_range, show_average, figure):
    start_month, end_month = date_range
    
    # Filter the data based on the selected date range
    filtered_data = data_noise[
        (data_noise["result_date"].dt.month >= start_month) &
        (data_noise["result_date"].dt.month <= end_month)
    ]
    
    # Update x and y values for the line chart
    x_values = filtered_data["result_date"]
    y_values = filtered_data["laeq"]
    
    # Remove existing average traces
    figure["data"] = [trace for trace in figure["data"] if "Average" not in trace["name"]]
    
    if "average" in show_average:
        # Calculate overall yearly average Laeq
        overall_average = data_noise["laeq"].mean()
        
        # Create a line trace for the overall yearly average
        overall_trace = go.Scatter(
            x=[min(x_values), max(x_values)],
            y=[overall_average, overall_average],
            mode="lines",
            name="Yearly Average",
            line=dict(color="red")
        )
        
        # Append the overall yearly average trace to the figure
        figure["data"].append(overall_trace)
    
    if "monthly" in show_average:
        # Calculate monthly average Laeq for each month
        monthly_average = filtered_data.groupby(filtered_data["result_date"].dt.month)["laeq"].mean()
        
        # Create a line trace for each month's average
        for month, average in monthly_average.items():
            # Filter the data to include only the corresponding month
            month_data = filtered_data[filtered_data["result_date"].dt.month == month]
            
            month_x_values = month_data["result_date"]
            month_y_values = [average] * len(month_x_values)
            
            month_trace = go.Scatter(
                x=month_x_values,
                y=month_y_values,
                mode="lines",
                name=f"Monthly Average - {pd.Timestamp(month=month, year=2022, day=1).strftime('%B')}",
                line=dict(color=plotly.colors.qualitative.D3[month % len(plotly.colors.qualitative.D3)])
            )
            
            # Append the monthly average trace to the figure
            figure["data"].append(month_trace)
    
    # Update x-axis range in the figure layout
    figure["layout"]["xaxis"]["range"] = [pd.Timestamp(year=2022, month=start_month, day=1),
                                          pd.Timestamp(year=2022, month=end_month, day=1)]
    
    return figure