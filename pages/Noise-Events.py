import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

#dash.register_page(__name__)

# Load data
data_noise = pd.read_csv("Data for visualization/combined_noise_event.csv", header=0, sep=',')

# Replace empty values with 'Missing'
data_noise['noise_event_laeq_primary_detected_class'] = data_noise['noise_event_laeq_primary_detected_class'].fillna('Missing')
data_noise['noise_event_laeq_primary_detected_certainty'] = data_noise['noise_event_laeq_primary_detected_certainty'].fillna(1)

# dropping the observations which did not record a noise source
#data_noise = data_noise.dropna(subset=['noise_event_laeq_primary_detected_class'])

# Drop observations with noise source 'unsupported'
#data_noise = data_noise[data_noise['noise_event_laeq_primary_detected_class'] != ('Unsupported', 'Transport road - Passenger car', 'Transport road - Siren', 'Nature elements - Wind','Missing')]

# Convert 'result_timestamp' column to datetime with the specified format
data_noise['result_timestamp'] = pd.to_datetime(data_noise['result_timestamp'], format='%Y-%m-%d %H:%M:%S.%f')

# Filter the data for January dates
#january_data = data_noise[data_noise['result_timestamp'].dt.month == 1]

# Filter the data based on certainty cutoff of 95%
data_noise = data_noise[data_noise['noise_event_laeq_primary_detected_certainty'] >= 95]

# Create figure
fig = go.Figure()

# Define colors for each category
category_colors = {
    'Human voice - Shouting': 'hotpink',
    'Music non-amplified': 'purple',
    'Human voice - Singing': 'pink',
    'Transport road - Passenger car' : 'blue',
    'Transport road - Siren' : 'orange',
    'Nature elements - Wind' : 'beige',
    'Unsupported' : 'black',
    'Missing': 'green'
}

categories = [
    'Human voice - Shouting',
    'Human voice - Singing',
    'Music non-amplified',
    'Transport road - Passenger car',
    'Transport road - Siren',
    'Nature elements - Wind',
    'Unsupported',
    'Missing',
]

for category in categories:
    # Create a horizontal line for the category
    fig.add_trace(go.Scatter(
        x=data_noise['result_timestamp'],
        y=[category] * len(data_noise),
        mode='lines',
        name=category,
        marker=dict(color=category_colors[category])
    ))

    # Filter the data for the current category
    category_data = data_noise[data_noise['noise_event_laeq_primary_detected_class'] == category]

    # Add scatter points for the category
    fig.add_trace(go.Scatter(
        x=category_data['result_timestamp'],
        y=category_data['noise_event_laeq_primary_detected_class'],
        mode='markers',
        marker=dict(
            size=20,  # Set the marker size to a constant number
            color=category_colors[category]
        ),
        name=category
    ))

# Create checkbox components
checkboxes = dcc.Checklist(
    id='category-checkboxes',
    options=[{'label': category, 'value': category} for category in categories],
    value=categories,  # All checkboxes are initially checked
    labelStyle={'display': 'block'}  # Display checkboxes vertically
)

# Create slider component
slider = dcc.RangeSlider(
    id='date-slider',
    min=data_noise['result_timestamp'].min().timestamp(),
    max=data_noise['result_timestamp'].max().timestamp(),
    value=[data_noise['result_timestamp'].min().timestamp(), data_noise['result_timestamp'].max().timestamp()],
    marks={timestamp.to_timestamp().timestamp(): {'label': timestamp.strftime('%d-%m-%Y'), 'style': {'transform': 'rotate(45deg)', 'white-space': 'nowrap'}}
           for timestamp in data_noise['result_timestamp'].dt.to_period('M').unique()},
    step=None
)

# Define layout
layout = html.Div([
    html.H2("What's causing the noise in Leuven?"),
    html.P("In order to trace the sources of noise events in the centre of Leuven, ..."),
    checkboxes,
    dcc.Graph(id='noise-plot', figure=fig),
    html.Div(slider)
])

# Define callbacks
@callback(
    Output('noise-plot', 'figure'),
    Input('date-slider', 'value'),
    Input('category-checkboxes', 'value')
)
def update_plot(date_range, selected_categories):
    min_timestamp = date_range[0]
    max_timestamp = date_range[1]

    filtered_data = data_noise[
        (data_noise['result_timestamp'].timestamp() >= min_timestamp) &
        (data_noise['result_timestamp'].timestamp() <= max_timestamp)
    ]

    fig = go.Figure()  # Create a new figure

    for category in selected_categories:
        category_data = filtered_data[filtered_data['noise_event_laeq_primary_detected_class'] == category]

        fig.add_trace(go.Scatter(
            x=category_data['result_timestamp'],
            y=category_data['noise_event_laeq_primary_detected_class'],
            mode='markers',
            marker=dict(
                size=2,  # Set the marker size to a constant number
                color=category_colors[category]
            ),
            name=category
        ))

    fig.update_layout(
        xaxis=dict(
            title='Date',
            tickformat='%d %b %Y',  # Format the x-axis tick labels as 'day month year'
            tickmode='linear',
            dtick='M1',  # Display one tick per month
            rangebreaks=[
                dict(pattern='day of week', bounds=[6, 1])  # Hide weekends on the x-axis
            ]
        ),
        yaxis=dict(
            title='Noise Source'
        ),
        title='Noise Source Visualization',
        width=1600,
        height=600,
        showlegend=True
    )

    return fig