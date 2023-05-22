import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import datetime

dash.register_page(__name__)

## Data ##
daily_noise = pd.read_csv("Data/daily_noisedata_2022.csv")
monthly_noise = pd.read_csv("Data/monthly_noisedata_2022.csv")

# Create dataframe with GPS coordinates
gps_data = {
    'description': ['MP 01: Naamsestraat 35  Maxim', 'MP 02: Naamsestraat 57 Xior', 'MP 03: Naamsestraat 62 Taste', 'MP 04: His & Hears', 'MP 05: Calvariekapel KU Leuven', 'MP 06: Parkstraat 2 La Filosovia', 'MP 07: Naamsestraat 81', 'MP08bis - Vrijthof'],
    'lat': [50.877121, 50.87650, 50.87590, 50.875237, 50.87452, 50.874078, 50.873808, 50.87873],
    'lon': [4.700708, 4.700632, 4.700262, 4.700071, 4.69985, 4.70005, 4.700007, 4.70115]
}

gps_df = pd.DataFrame(gps_data)

# Merging noise data with GPS coordinates
merged = pd.merge(daily_noise, gps_df, on='description', how='left')

# Add a new column 'year' with value 2022 for all observations
merged['year'] = 2022
# Create a new 'date' column by combining 'year', 'month', and 'day' but put the date in the European way
merged['date'] = pd.to_datetime(merged[['year', 'month', 'day']]).dt.strftime('%d %b %Y')

# Create a StandardScaler object
scaler = MinMaxScaler()

# Fit the StandardScaler to the column and transform the Lamax and laeq values
merged['standardized_lamax'] = scaler.fit_transform(merged[['lamax']])
merged['standardized_laeq'] = scaler.fit_transform(merged[['laeq']])

## Lamax map ##
fig_lamax = px.scatter_mapbox(merged, 
                              lat='lat', 
                              lon='lon', 
                              size='standardized_lamax',
                              size_max=30,
                              animation_frame="date",
                              zoom=4,
                              mapbox_style='open-street-map')

# Set the initial center and zoom level of the map
fig_lamax.update_layout(mapbox={
    'center': {'lat': 50.876, 'lon': 4.699850},
    'zoom': 15
},
height=800,
width=800, 
margin=dict(l=20, r=400, t=0, b=100)
)

## Laeq map ##
fig_laeq = px.scatter_mapbox(merged, 
                             lat='lat', 
                             lon='lon', 
                             size='standardized_laeq',
                             size_max=30,
                             animation_frame="date",
                             zoom=4,
                             mapbox_style='open-street-map')

# Set the initial center and zoom level of the map
fig_laeq.update_layout(mapbox={
    'center': {'lat': 50.876, 'lon': 4.699850},
    'zoom': 15
},
height=800,
width=800, 
margin=dict(l=20, r=400, t=0, b=100)
)

def marker_click_lamax(trace, points, state):
    # Get the clicked marker information
    lat = trace.lat[points.point_inds[0]]
    lon = trace.lon[points.point_inds[0]]
    size = trace.marker.size[points.point_inds[0]]

    # Retrieve the value from the 'standardized_lamax' column
    value = merged.loc[points.point_inds[0], 'standardized_lamax']

def marker_click_laeq(trace, points, state):
    # Get the clicked marker information
    lat = trace.lat[points.point_inds[0]]
    lon = trace.lon[points.point_inds[0]]
    size = trace.marker.size[points.point_inds[0]]

    # Retrieve the value from the 'standardized_laeq' column
    value = merged.loc[points.point_inds[0], 'standardized_laeq']

# Assign the callback functions to the scattermapbox traces
fig_lamax.data[0].on_click(marker_click_lamax)
fig_laeq.data[0].on_click(marker_click_laeq)

# Update the 'text' parameter in px.scatter_mapbox
def update_hover_text(selected_map):
    if selected_map == "Lamax":
        selected_column = "standardized_lamax"
        fig = fig_lamax
    else:
        selected_column = "standardized_laeq"
        fig = fig_laeq

    # Retrieve the values from the selected column
    selected_column_values = merged[selected_column]

    # Update the 'text' parameter in the selected map
    fig.update_traces(text=[
        f"Date: {date}<br>Latitude: {lat}<br>Longitude: {lon}<br>{selected_map}: {value}"
        for date, lat, lon, value in zip(merged['date'], merged['lat'], merged['lon'], selected_column_values)
    ])

# Update the initial hover text based on the selected map
update_hover_text("Lamax")

layout = html.Div([
    html.H1(children='Noise map with sound monitor locations'),
    dcc.Dropdown(
        id="selected-map",
        options=[
            {'label': 'Lamax', 'value': 'Lamax'},
            {'label': 'Laeq', 'value': 'Laeq'}
        ],
        value='Lamax',
        style={'width': '200px'}
    ),
    dcc.Graph(id="noise-map", style={'width': '80%', 'height': '80vh', 'margin': 'auto'})  # Adjust the width as needed,
], 
style={'display': 'flex', 'justify-content': 'space-between'})

@callback(
    Output("noise-map", "figure"),
    [Input("selected-map", "value")]
)
def update_map(selected_map):
    if selected_map == "Lamax":
        return fig_lamax
    else:
        return fig_laeq