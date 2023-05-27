import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

dash.register_page(__name__)

# Load data
data_noise = pd.read_csv("Data/csv_results_41_255441_mp-03-naamsestraat-62-taste.csv", header=0, sep=';')

# dropping the observations which did not record a noise source
data_noise = data_noise.dropna(subset=['noise_event_laeq_primary_detected_class'])

# Drop observations with noise source 'unsupported'
data_noise = data_noise[data_noise['noise_event_laeq_primary_detected_class'] != ('Unsupported', 'Transport road - Passenger car', 'Transport road - Siren', 'Nature elements - Wind')]

# Convert 'result_timestamp' column to datetime with the specified format
data_noise['result_timestamp'] = pd.to_datetime(data_noise['result_timestamp'], format='%d/%m/%Y %H:%M:%S.%f')

# Filter the data for January dates
january_data = data_noise[data_noise['result_timestamp'].dt.month == 1]


# Create figure
fig = go.Figure()

# Define colors for each category
category_colors = {
    'Human voice - Shouting': 'hotpink',
    'Music non-amplified': 'purple',
    'Human voice - Singing': 'pink',
}

categories = ['Human voice - Shouting', 'Human voice - Singing', 'Music non-amplified']

for category in categories:
    # Create a horizontal line for the category
    fig.add_trace(go.Scatter(
        x=january_data['result_timestamp'],
        y=[category] * len(january_data),
        mode='lines',
        name=category,
        marker=dict(color=category_colors[category])
    ))

    # Filter the data for the current category
    category_data = january_data[january_data['noise_event_laeq_primary_detected_class'] == category]

    # Add scatter points for the category
    fig.add_trace(go.Scatter(
        x=category_data['result_timestamp'],
        y=category_data['noise_event_laeq_primary_detected_class'],
        mode='markers',
        marker=dict(
            size=category_data['noise_event_laeq_primary_detected_certainty'],
            sizemode='area',
            sizeref=0.1,
            color=category_colors[category]
        ),
        name=category
    ))

# Create slider component
slider = dcc.Slider(
    id='date-slider',
    min=data_noise['result_timestamp'].min().timestamp(),
    max=data_noise['result_timestamp'].max().timestamp(),
    value=data_noise['result_timestamp'].min().timestamp(),
    marks={timestamp.to_timestamp().timestamp(): {'label': timestamp.strftime('%d-%m-%Y'), 'style': {'transform': 'rotate(45deg)', 'white-space': 'nowrap'}}
           for timestamp in data_noise['result_timestamp'].dt.to_period('M').unique()},
    step=None
)

# Define layout
layout = html.Div([
    html.H2("What's causing the noise in Leuven?"),
    html.P("In order to trace the sources of noise events in the centre of Leuven, ..."),
    dcc.Graph(id='noise-plot', figure=fig),
    html.Div(slider)
])

# Define callbacks
@callback(
    Output('noise-plot', 'figure'),
    Input('date-slider', 'value')
)
def update_plot(selected_timestamp):
    selected_date = datetime.datetime.fromtimestamp(selected_timestamp)
    filtered_data = data_noise[data_noise['result_timestamp'].dt.month == selected_date.month]
    
    fig = go.Figure()  # Create a new figure
    
    for category in categories:
        category_data = filtered_data[filtered_data['noise_event_laeq_primary_detected_class'] == category]
        
        fig.add_trace(go.Scatter(
            x=category_data['result_timestamp'],
            y=category_data['noise_event_laeq_primary_detected_class'],
            mode='markers',
            marker=dict(
                size=category_data['noise_event_laeq_primary_detected_certainty'],
                sizemode='area',
                sizeref=0.1,
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
