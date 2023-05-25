import dash
from dash import dcc, html, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State

dash.register_page(__name__)

# Loading noise data
data_noise = pd.read_csv('Data/daily_noisedata_2022.csv', header=0, sep=',')
data_noise.head()

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

# Line chart visualization
fig = px.line(data_noise, x="result_date", y="laeq", title="Laeq Over Time")

# Defining the app layout
layout = html.Div(
    children=[
        html.H2("Noise Level Analysis"),
        html.P("To analyze the noise levels in Leuven over time, we constructed a time series model."),
        dcc.Graph(id="noise-graph", figure=fig),
        dcc.RangeSlider(
            id="date-slider",
            marks={i: pd.Timestamp(year=2022, month=i, day=1).strftime("%B") for i in range(1, 13)},
            min=1,
            max=12,
            value=[1, 12],
            step=1,
        ),
        dcc.Checklist(id='average-checkbox', options=[{'label': 'Show Yearly Average', 'value': 'average'}], value=[])
    ]
)

@callback(
    Output("noise-graph", "figure"),
    [Input("date-slider", "value"), Input("average-checkbox", "value")],
    [State("noise-graph", "figure")]
)

def update_graph(date_range, show_average, figure):
    start_month, end_month = date_range
    filtered_data = data_noise[
        (data_noise["result_date"].dt.month >= start_month) &
        (data_noise["result_date"].dt.month <= end_month)
    ]
    
    # Create a range of dates for each selected month
    months = pd.date_range(start=f"2022-{start_month}-01", end=f"2022-{end_month}-01", freq="MS")
    x_values = []
    y_values = []
    
    for month in months:
        month_data = filtered_data[filtered_data["result_date"].dt.month == month.month]
        x_values.extend(month_data["result_date"])
        y_values.extend(month_data["laeq"])
    
    # Update the scatter trace with new x and y values
    figure["data"][0]["x"] = x_values
    figure["data"][0]["y"] = y_values
    
    if show_average:
        # Calculate average Laeq for the selected month range
        average_laeq = filtered_data["laeq"].mean()
        
        # Create a line trace for the average Laeq
        average_trace = go.Scatter(x=[min(x_values), max(x_values)], y=[average_laeq, average_laeq],
                                   mode="lines", name="Average Laeq", line=dict(color="red"))
        
        # Check if the average trace already exists, and update or append accordingly
        average_trace_exists = any(trace["name"] == "Average Laeq" for trace in figure["data"])
        
        if average_trace_exists:
            # Update the existing average trace
            figure["data"] = [trace if trace["name"] != "Average Laeq" else average_trace for trace in figure["data"]]
        else:
            # Append the average trace
            figure["data"].append(average_trace)
    else:
        # Remove average line if checkbox is unchecked
        figure["data"] = [trace for trace in figure["data"] if trace["name"] != "Average Laeq"]
    
    figure["layout"]["title"] = "Noise Levels Over Time (Naamsestraat 62 Taste)"
    figure["layout"]["yaxis"]["title"] = "Noise Level (Laeq in dB(A))"
    figure["layout"]["xaxis"]["title"] = "" #title can be added but I think it's more clear without one, the dates are shown on the axis 
    return figure
