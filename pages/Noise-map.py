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
merged_daily = pd.merge(daily_noise, gps_df, on='description', how='left')
merged_monthly = pd.merge(monthly_noise, gps_df, on='description', how='left')

# Add a new column 'year' with value 2022 for all observations
merged_daily['year'] = 2022
# Create a new 'date' column by combining 'year', 'month', and 'day' but put the date in the European way
merged_daily['date'] = pd.to_datetime(merged_daily[['year', 'month', 'day']]).dt.strftime('%d %b %Y')

# Convert numeric month to month names
merged_monthly['month'] = pd.to_datetime(merged_monthly['month'], format='%m').dt.strftime('%B')

# Create a StandardScaler object
scaler = MinMaxScaler()
# Fit the StandardScaler to the column and transform the Lamax and laeq values
merged_daily['standardized_lamax'] = scaler.fit_transform(merged_daily[['lamax']])
merged_daily['standardized_laeq'] = scaler.fit_transform(merged_daily[['laeq']])
merged_monthly['standardized_lamax'] = scaler.fit_transform(merged_monthly[['lamax']])
merged_monthly['standardized_laeq'] = scaler.fit_transform(merged_monthly[['laeq']])


## Laeq map daily ##
fig_laeq_daily = px.scatter_mapbox(merged_daily, 
                                   lat='lat', 
                                   lon='lon', 
                                   size='standardized_laeq',
                                   size_max=30,
                                   animation_frame="date",
                                   zoom=4,
                                   mapbox_style='open-street-map',
                                   hover_data={'lat': False, 'lon': False, 'date': True, 'description': True, 
                                               'laeq': True, 'standardized_laeq': True})
# Set the initial center and zoom level of the map
fig_laeq_daily.update_layout(mapbox={
    'center': {'lat': 50.876, 'lon': 4.70020},
    'zoom': 15
},
height=800,
width=800, 
margin=dict(l=20, r=400, t=0, b=100)
)

## Lamax map daily ##
fig_lamax_daily = px.scatter_mapbox(merged_daily, 
                                    lat='lat', 
                                    lon='lon', 
                                    size='standardized_lamax',
                                    size_max=30,
                                    animation_frame="date",
                                    zoom=4,
                                    mapbox_style='open-street-map',
                                    hover_data={'lat': False, 'lon': False, 'date': True, 'description': True, 
                                               'lamax': True, 'standardized_lamax': True})
# Set the initial center and zoom level of the map
fig_lamax_daily.update_layout(mapbox={
    'center': {'lat': 50.876, 'lon': 4.70020},
    'zoom': 15
},
height=800,
width=800, 
margin=dict(l=20, r=400, t=0, b=100)
)

## Lamax map monthly ##
fig_lamax_monthly = px.scatter_mapbox(merged_monthly, 
                                      lat='lat', 
                                      lon='lon', 
                                      size='standardized_lamax',
                                      size_max=30,
                                      animation_frame="month",
                                      zoom=4,
                                      mapbox_style='open-street-map',
                                      hover_data={'lat': False, 'lon': False, 'month': True, 'description': True, 
                                                  'lamax': True, 'standardized_lamax': True})
# Set the initial center and zoom level of the map
fig_lamax_monthly.update_layout(mapbox={
    'center': {'lat': 50.876, 'lon': 4.70020},
    'zoom': 15
},
height=800,
width=800, 
margin=dict(l=20, r=400, t=0, b=100)
)

## Laeq map monthly ##
fig_laeq_monthly = px.scatter_mapbox(merged_monthly, 
                                     lat='lat', 
                                     lon='lon', 
                                     size='standardized_laeq',
                                     size_max=30,
                                     animation_frame="month",
                                     zoom=4,
                                     mapbox_style='open-street-map',
                                     hover_data={'lat': False, 'lon': False, 'month': True, 'description': True, 
                                                  'laeq': True, 'standardized_laeq': True})
# Set the initial center and zoom level of the map
fig_laeq_monthly.update_layout(mapbox={
    'center': {'lat': 50.876, 'lon': 4.70020},
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
#fig_lamax.data[0].on_click(marker_click_lamax)
#fig_laeq.data[0].on_click(marker_click_laeq)


def update_hover_text(selected_map, selected_period):
    if selected_period == "Daily":
        if selected_map == "Lamax":
            selected_column = "lamax"
            selected_level = "Lamax"
            selected_standardized_column = "standardized_lamax"
            selected_dates = merged_daily['date']
        else:
            selected_column = "laeq"
            selected_level = "Laeq"
            selected_standardized_column = "standardized_laeq"
            selected_dates = merged_daily['date']
    else:
        if selected_map == "Lamax":
            selected_column = "lamax"
            selected_level = "Lamax"
            selected_standardized_column = "standardized_lamax"
            selected_dates = merged_monthly['month']
        else:
            selected_column = "laeq"
            selected_level = "Laeq"
            selected_standardized_column = "standardized_laeq"
            selected_dates = merged_monthly['month']

    # Retrieve the values from the selected columns
    selected_column_values = merged_daily[selected_column] if selected_period == "Daily" else merged_monthly[selected_column]
    selected_standardized_column_values = merged_daily[selected_standardized_column] if selected_period == "Daily" else merged_monthly[selected_standardized_column]
    selected_locations = merged_daily['description'] if selected_period == "Daily" else merged_monthly['description']

    # Update the 'text' parameter in the selected map
    if selected_period == "Daily":
        fig_lamax_daily.update_traces(text=[
            f"Date: {date}<br>Location: {location}<br>Noise Level: {selected_level}: {level} dB(A)<br>Standardized Noise Level: {standardized_level} dB(A)"
            for date, location, level, standardized_level in zip(selected_dates, selected_locations, selected_column_values, selected_standardized_column_values)
        ])
        fig_laeq_daily.update_traces(text=[
            f"Date: {date}<br>Location: {location}<br>Noise Level: {selected_level}: {level} dB(A)<br>Standardized Noise Level: {standardized_level} dB(A)"
            for date, location, level, standardized_level in zip(selected_dates, selected_locations, selected_column_values, selected_standardized_column_values)
        ])
    else:
        fig_lamax_monthly.update_traces(text=[
            f"Month: {date}<br>Location: {location}<br>Noise Level: {selected_level}: {level} dB(A)<br>Standardized Noise Level: {standardized_level} dB(A)"
            for date, location, level, standardized_level in zip(selected_dates, selected_locations, selected_column_values, selected_standardized_column_values)
        ])
        fig_laeq_monthly.update_traces(text=[
            f"Month: {date}<br>Location: {location}<br>Noise Level: {selected_level}: {level} dB(A)<br>Standardized Noise Level: {standardized_level} dB(A)"
            for date, location, level, standardized_level in zip(selected_dates, selected_locations, selected_column_values, selected_standardized_column_values)
        ])


# Update the initial hover text based on the selected map
#update_hover_text("Lamax", "Daily")

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
    dcc.RadioItems(
    id="selected-period",
    options=[
        {'label': 'Daily', 'value': 'Daily'},
        {'label': 'Monthly', 'value': 'Monthly'}
    ],
    value='Daily',
    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
    style={'font-size': '20px'}    
    ),
    dcc.Graph(id="noise-map", style={'width': '50%', 'height': '80vh', 'margin': 'auto'})  
], 
style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})


@callback(
    Output("noise-map", "figure"),
    [Input("selected-map", "value"),
     Input("selected-period", "value")]
)
def update_map(selected_map, selected_period):
    if selected_period == "Daily":
        if selected_map == "Lamax":
            return fig_lamax_daily
        else:
            return fig_laeq_daily
    else:
        if selected_map == "Lamax":
            return fig_lamax_monthly
        else:
            return fig_laeq_monthly
    # Call update_hover_text to update the hover text
    update_hover_text(selected_map, selected_period)
