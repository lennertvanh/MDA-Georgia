#########################################################################################################
# PACKAGES

import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__)

#########################################################################################################
# DATA

# Load data
data_noise = pd.read_csv("Data for visualization/combined_noise_event.csv", header=0, sep=',')

# Replace empty values with 'Missing'
data_noise['noise_event_laeq_primary_detected_class'] = data_noise['noise_event_laeq_primary_detected_class'].fillna('Missing')

# Compute average noise level (laeq) for each noise source category
data_noise = data_noise.groupby('noise_event_laeq_primary_detected_class')['laeq'].mean().reset_index()

# Sort the dataset based on 'laeq'
data_noise = data_noise.sort_values(by='laeq')

#########################################################################################################
# VISUALIZATION

# Create figure
fig = go.Figure()

category_colors = {
    'Human voice - Shouting': 'hotpink',
    'Music non-amplified': 'purple',
    'Human voice - Singing': 'orange',
    'Transport road - Passenger car' : 'blue',
    'Transport road - Siren' : 'red',
    'Nature elements - Wind' : 'lightblue',
    'Unsupported' : 'black',
    'Missing' : 'green'
}

categories = [
    'Human voice - Singing',
    'Nature elements - Wind',
    'Transport road - Siren',
    'Human voice - Shouting',
    'Unsupported',
    'Missing',
    'Music non-amplified',
    'Transport road - Passenger car',
]

for category in categories:
    category_data = data_noise[data_noise['noise_event_laeq_primary_detected_class'] == category]
    x_values = category_data['laeq']
    
    # Add a horizontal line trace for each category
    fig.add_trace(go.Scatter(
        x=[x_values.iloc[0], x_values.iloc[-1]],
        y=[category],
        mode='lines',
        name=category,
        line=dict(color='red', width=1),
        showlegend=False,
    ))

    # Add circle markers for each category
    fig.add_trace(go.Scatter(
        x=x_values,
        y=[category] * len(x_values),
        mode='markers',
        marker=dict(
            size=30,
            sizemode='diameter',
            color='red',
        ),
        name=category,
        showlegend=False,
        hovertemplate='<b>Average Noise Level</b>: %{x:.2f} dB(A)<br>' +
                      '<b>Noise Source</b>: %{y}<extra></extra>',
    ))

fig.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    title=dict(
                text="Average noise level per noise source",
                font=dict(color="white"),
            ),
            title_font=dict(size=24),
            xaxis=dict(
                title="Average noise level (in dB(A))",
                title_font=dict(color="white", size =18),
                tickfont=dict(color="white"),
                gridcolor='rgba(255, 255, 255, 0.1)',
            ),
        yaxis=dict(
            tickfont=dict(color="white"),
            gridcolor='rgba(255, 255, 255, 0.1)'
            ),
        margin=dict(l=50, r=50, t=50, b=50),
)

#########################################################################################################
# PAGE LAYOUT

layout = html.Div([
    html.H2("Which source causes the loudest noise on average?"),
    html.P("We previously discovered that the most frequently occurring source of noise in the city of Leuven was cars, but are they also the loudest? In the figure below, the average noise level is displayed for each noise source. It turns out cars are actually the most quiet one out of these noise sources."),
    html.Div(
        className="plot-container",
        style={'padding': '20px', 'max-width': '90vw', 'justify-content': 'center'},
        children=[
            dcc.Graph(
                id='noise-source-laeq', 
                figure=fig
                ),
        ],
    ),
],
)