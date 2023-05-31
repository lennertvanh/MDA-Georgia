import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler

dash.register_page(__name__)

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

# Aggregate the data by day and noise class
daily_counts = data_noise.groupby([data_noise['result_timestamp'].dt.date, 'noise_event_laeq_primary_detected_class']).size().reset_index(name='count')

# Standardize the count values
scaler = StandardScaler()
daily_counts['count_scaled'] = scaler.fit_transform(daily_counts[['count']])

# Convert result_timestamp to datetime.date format for comparison
daily_counts['result_timestamp'] = pd.to_datetime(daily_counts['result_timestamp']).dt.date

# Create figure
fig = go.Figure()

# Define colors for each category
category_colors = {
    'Human voice - Shouting': 'hotpink',
    'Music non-amplified': 'purple',
    'Human voice - Singing': 'pink',
    'Transport road - Passenger car' : 'blue',
    'Transport road - Siren' : 'orange',
    'Nature elements - Wind' : 'lightblue',
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
            sizeref=0.1,
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

# Create a list of all the months between the minimum and maximum dates
months = pd.date_range(start=start_date, end=max_date, freq='MS')

# Generate marks for each month
marks = {date.toordinal(): {'label': date.strftime('%b %Y')} for date in months}


layout = html.Div([
    html.H2("What's causing the noise in Leuven?"),
    html.P("In order to trace the sources of noise events in the centre of Leuven, ..."),
    dcc.Graph(id='noise-plot', figure=fig),
    dcc.RangeSlider(
        id='date-slider',
        min=min_value,
        max=max_date.toordinal(),
        value=[min_value, max_date.toordinal()],
        marks=marks,
            #{timestamp.to_timestamp().date().toordinal(): {'label': timestamp.strftime('%b %Y')}
            #for timestamp in data_noise['result_timestamp'].dt.to_period('M').unique()},
            #{timestamp.to_timestamp().date().toordinal(): {'label': timestamp.strftime('%d-%m-%Y'), 'style': {'transform': 'rotate(45deg)', 'white-space': 'nowrap'}}
            #for timestamp in data_noise['result_timestamp'].dt.to_period('D').unique()
        step=None
    ),
    dcc.Checklist(
        id='category-checkboxes',
        options=[{'label': category, 'value': category} for category in categories],
        value=categories,  # All checkboxes are initially checked
        labelStyle={'display': 'block'}  # Display checkboxes vertically
    ),
    dcc.Store(id='selected-categories')
])

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
    max_date = datetime.fromordinal(max_ordinal).date() + timedelta(days=1)  # Add 1 day to include the end date

    min_timestamp = pd.Timestamp(min_date)
    max_timestamp = pd.Timestamp(max_date)

    daily_counts['result_timestamp'] = pd.to_datetime(daily_counts['result_timestamp'])  # Convert to datetime data type

    filtered_data = daily_counts[
        (daily_counts['result_timestamp'].dt.date >= min_timestamp.date()) &
        (daily_counts['result_timestamp'].dt.date <= max_timestamp.date()) &
        (daily_counts['noise_event_laeq_primary_detected_class'].isin(selected_categories))
    ]

    fig = go.Figure()  # Create a new figure

    for category in selected_categories:
        category_data = filtered_data[filtered_data['noise_event_laeq_primary_detected_class'] == category]

        fig.add_trace(go.Scatter(
            x=category_data['result_timestamp'],
            y=category_data['noise_event_laeq_primary_detected_class'],
            mode='markers',
            marker=dict(
                size=category_data['count_scaled'].abs(),
                sizeref=0.1,
                color=category_colors[category]
            ),
            name=category
        ))

    fig.update_xaxes(range=[min_timestamp, max_timestamp], tickformat='%d-%m-%Y')

    return fig