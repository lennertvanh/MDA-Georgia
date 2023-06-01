#########################################################################################################
# PACKAGES

import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import datetime, timedelta
import numpy as np

dash.register_page(__name__)

#########################################################################################################
# DATA

# Load data
data_noise = pd.read_csv("Data for visualization/combined_noise_event.csv", header=0, sep=',')

# Replace empty values with 'Missing'
data_noise['noise_event_laeq_primary_detected_class'] = data_noise['noise_event_laeq_primary_detected_class'].fillna('Missing')
data_noise['noise_event_laeq_primary_detected_certainty'] = data_noise['noise_event_laeq_primary_detected_certainty'].fillna(1)

# Convert 'result_timestamp' column to datetime with the specified format
data_noise['result_timestamp'] = pd.to_datetime(data_noise['result_timestamp'], format='%Y-%m-%d %H:%M:%S.%f')

# Filter the data based on certainty cutoff of 95%
data_noise = data_noise[data_noise['noise_event_laeq_primary_detected_certainty'] >= 95]

# Aggregate the data by day and noise class
daily_counts = data_noise.groupby([data_noise['result_timestamp'].dt.date, 'noise_event_laeq_primary_detected_class']).size().reset_index(name='count')

# Convert result_timestamp to datetime.date format for comparison
daily_counts['result_timestamp'] = pd.to_datetime(daily_counts['result_timestamp']).dt.date

### CREATE SCALER FOR SIZES OF CIRCLE MARKERS (proportional to the daily count) ###
max_count = daily_counts["count"].max()
min_count = daily_counts["count"].min()

start_size = 0.4 #minimum size
step_size = 4.8 #maximum size 

def divide_by_max(x):
    return x / max_count

def myMapping(x):
    return start_size + step_size*(x-min_count)/(max_count-min_count)

daily_counts['count_scaled'] = daily_counts['count'].transform(myMapping)

#########################################################################################################
# VISUALIZATION

# Create figure
fig = go.Figure()

# Define colors for each category
category_colors = {
    'Human voice - Shouting': 'hotpink',
    'Music non-amplified': 'red',
    'Human voice - Singing': '#EB862E',
    'Transport road - Passenger car' : '#2A9D8F',
    'Transport road - Siren' : '#E6AF2E',
    'Nature elements - Wind' : 'white',
}

categories = [
    'Human voice - Shouting',
    'Human voice - Singing',
    'Music non-amplified',
    'Transport road - Passenger car',
    'Transport road - Siren',
    'Nature elements - Wind',
]

for category in categories:
    # Create a horizontal line for the category
    fig.add_trace(go.Scatter(
        x=daily_counts[daily_counts['noise_event_laeq_primary_detected_class'] == category]['result_timestamp'],
        y=[category] * len(daily_counts[daily_counts['noise_event_laeq_primary_detected_class'] == category]),
        mode='lines',
        name=category,
        marker=dict(color=category_colors[category])
    ))

    # Add scatter points for the category
    fig.add_trace(go.Scatter(
        x=daily_counts[daily_counts['noise_event_laeq_primary_detected_class'] == category]['result_timestamp'],
        y=daily_counts[daily_counts['noise_event_laeq_primary_detected_class'] == category]['noise_event_laeq_primary_detected_class'],
        mode='markers',
        marker=dict(
            size=daily_counts[daily_counts['noise_event_laeq_primary_detected_class'] == category]['count_scaled'].abs(),
            sizeref=0.045,
            color=category_colors[category]
        ),
        name=category
    ))

# Set x-axis range and format
fig.update_xaxes(range=[data_noise['result_timestamp'].min(), data_noise['result_timestamp'].max()], tickformat='%d-%m-%Y')

# Find the minimum and maximum dates in the data
min_date = data_noise['result_timestamp'].min().date()
max_date = data_noise['result_timestamp'].max().date()

# Set the start date as January 2022
start_date = pd.Timestamp(year=2022, month=1, day=1)
min_value = start_date.toordinal()

# Set the end date as December 2022
end_date = pd.Timestamp(year=2023, month=1, day=1)
max_value = end_date.toordinal()

# Create a list of all the months between the minimum and maximum dates
months = pd.date_range(start=start_date, end=end_date, freq='MS')  # Change max_date to end_date

# Generate marks for each month
marks = {date.toordinal(): {'label': date.strftime('%b %Y')} for date in months}

fig.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)'
)

#########################################################################################################
# PAGE LAYOUT

layout = html.Div([
    html.H2("What's causing the noise in Leuven?"),
    html.P("We have observed that students likely play a significant role in contributing to the noise in Leuven. However, the data also provides insights regarding the sources of the observed sounds. To better understand and trace the various noise sources in Leuven, we present a bubble chart, which showcases the different potential noise sources and their frequencies over time. The size of each circle corresponds to the frequency of sound observations on a particular day, offering a dynamic portrayal of noise patterns in the city. Humans and traffic are the most prominent noise sources."),
    html.Div(
        className="plot-container",
        style={'padding': '20px', 'max-width': '90vw', 'justify-content': 'center'},
        children=[
            dcc.Graph(
                id='noise-plot', 
                figure=fig
                ),
            dcc.RangeSlider(
                className='slider-white',
                id='date-slider',
                min=min_value,
                max=max_value,
                value=[min_value,  max_value],
                marks=marks,
                step=None
            ),
            dcc.Checklist(
                id='category-checkboxes',
                options=[{'label': category, 'value': category} for category in categories],
                value=categories,  # All checkboxes are initially checked
                labelStyle={'display': 'block'}  # Display checkboxes vertically
            ),
        ]
    ),
    dcc.Store(id='selected-categories')
])

#########################################################################################################
# CALLBACK UPDATE GRAPH

# Define callbacks
@callback(
    Output('selected-categories', 'data'),
    Input('category-checkboxes', 'value')
)
def store_selected_categories(selected_categories):
    return selected_categories


@callback(
    Output('noise-plot', 'figure'),
    Input('date-slider', 'value'),
    Input('selected-categories', 'data')
)
def update_plot(date_range, selected_categories):
    min_ordinal = date_range[0]
    max_ordinal = date_range[1]

    min_date = datetime.fromordinal(min_ordinal).date()
    max_date = datetime.fromordinal(max_ordinal).date()  # Remove the "+ timedelta(days=1)" here

    filtered_data = daily_counts[
        (daily_counts['result_timestamp'] >= min_date) &
        (daily_counts['result_timestamp'] <= max_date) &
        (daily_counts['noise_event_laeq_primary_detected_class'].isin(selected_categories))
    ].copy()

    fig = go.Figure()  # Create a new figure

    for category in selected_categories:
        category_data = filtered_data[filtered_data['noise_event_laeq_primary_detected_class'] == category]

        fig.add_trace(go.Scatter(
            x=category_data['result_timestamp'],
            y=category_data['noise_event_laeq_primary_detected_class'],
            mode='markers',
            text = category_data['count'].astype(str), 
            marker=dict(
                size=category_data['count_scaled'].abs(),
                sizeref=0.045,
                color=category_colors[category],
            ),
            name=category,
            showlegend=False,
            hovertemplate='<b>Date</b>: %{x|%d-%m-%Y}<br>' +
                          '<b>Noise Source</b>: %{y}<br>' +
                          '<b>Count</b>: %{text}<extra></extra>' 
        ))

    fig.update_xaxes(range=[min_date, max_date], tickformat='%d-%m-%Y')

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        title=dict(
            text="Sources of noise events per day in 2022 (circle size proportional to frequency)",
            font=dict(color="white"),
        ),
        title_font=dict(size=24),
        xaxis=dict(
            title="Date",
            title_font=dict(color="white", size=18),
            tickfont=dict(color="white"),
            gridcolor='rgba(255, 255, 255, 0.1)',
        ),
        yaxis=dict(
            tickfont=dict(color="white"),
            gridcolor='rgba(255, 255, 255, 0.1)'
        ),
        margin=dict(l=50, r=50, t=50, b=50),
    )

    return fig
