import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler


dash.register_page(__name__)

## Data ##
monthly_noise = pd.read_csv("Data/monthly_noisedata_2022.csv")

# Create dataframe with GPS coordinates 
gps_data = {
    'description': ['MP 01: Naamsestraat 35  Maxim', 'MP 02: Naamsestraat 57 Xior', 'MP 03: Naamsestraat 62 Taste', 'MP 04: His & Hears', 'MP 05: Calvariekapel KU Leuven', 'MP 06: Parkstraat 2 La Filosovia', 'MP 07: Naamsestraat 81', 'MP08bis - Vrijthof'],
    'lat': [50.877121, 50.87650, 50.87590, 50.875237, 50.87452, 50.874078, 50.873808, 50.87873],
    'lon': [4.700708, 4.700632, 4.700262, 4.700071, 4.69985, 4.70005, 4.700007, 4.70115]
}

gps_df = pd.DataFrame(gps_data)

# Merging noise data with GPS coordinates
merged = pd.merge(monthly_noise, gps_df, on='description', how='left')

# Create a StandardScaler object
scaler = MinMaxScaler()

# Fit the StandardScaler to the column and transform the Lamax values
merged['standardized_lamax'] = scaler.fit_transform(merged[['lamax']])

# Fit the StandardScaler to the column and transform the Lamax values
merged['standardized_laeq'] = scaler.fit_transform(merged[['laeq']])

merged.head()

# Check for missing values in each column
#print(merged.isnull().sum())


## Noise map ##

# Add initial trace to the figure
fig = px.scatter_mapbox(merged, 
                        lat = 'lat', 
                        lon = 'lon', 
                        size = 'standardized_lamax',
                        size_max = 30,
                        animation_frame="month",
                        zoom = 4, mapbox_style = 'open-street-map'
                        )


# Set the initial center and zoom level of the map
fig.update_layout(mapbox={
    'center': {'lat': 50.876, 'lon': 4.699850},
    'zoom': 15
},
height=800,
width=800, 
margin=dict(l=20, r=400, t=0, b=100)
)

def marker_click(trace, points, state):
    # Get the clicked marker information
    lat = trace.lat[points.point_inds[0]]
    lon = trace.lon[points.point_inds[0]]
    size = trace.marker.size[points.point_inds[0]]
    text = trace.text[points.point_inds[0]]

    # Perform actions based on the clicked marker
    # For example, display a pop-up or generate a new visualization

# Assign the callback function to the scattermapbox trace
fig.data[0].on_click(marker_click)

# Add dropdown for switching between Lamax and Laeq
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=[{"marker.size": merged['standardized_lamax']}],
                    label="Lamax",
                    method="restyle"
                ),
                dict(
                    args=[{"marker.size": merged['standardized_laeq']}],
                    label="Laeq",
                    method="restyle"
                )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.0,
            xanchor="left",
            y=1.3,
            yanchor="top"
        ),
    ]
)

layout = html.Div(children=[
    html.H1(children='Noise map with sound monitor locations'),

    dcc.Graph(id="noise-map", figure=fig, style={'width': '80%', 'height': '80vh','margin': 'auto'})  # Adjust the width as needed,

])