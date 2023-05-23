import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import datetime

#dash.register_page(__name__)

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

# Convert numeric month to month names (in a column date to use same name as above)
merged_monthly['date'] = pd.to_datetime(merged_monthly['month'], format='%m').dt.strftime('%B')

# Create a StandardScaler object
scaler = MinMaxScaler()
# Fit the StandardScaler to the column and transform the Lamax and laeq values
merged_daily['standardized_lamax'] = scaler.fit_transform(merged_daily[['lamax']])
merged_daily['standardized_laeq'] = scaler.fit_transform(merged_daily[['laeq']])
merged_monthly['standardized_lamax'] = scaler.fit_transform(merged_monthly[['lamax']])
merged_monthly['standardized_laeq'] = scaler.fit_transform(merged_monthly[['laeq']])


## Laeq map daily ##
# Create the Scattermapbox trace
data_trace = go.Scattermapbox(
    lat=merged_daily['lat'],
    lon=merged_daily['lon'],
    mode='markers',
    marker=dict(
        size=merged_daily['standardized_laeq'],
        sizemode='diameter',
        sizeref=0.1,
        color='blue'
    ),
    customdata=merged_daily[['date', 'description', 'laeq', 'standardized_laeq']],
    hoverlabel=dict(namelength=0),
    hovertemplate='Date: %{customdata[0]}<br>'
                  'Location: %{customdata[1]}<br>'
                  'Noise level: %{customdata[2]:.2f} dB(A)<br>'
                  'Standardized noise level: %{customdata[3]:.2f} dB(A)'
)
# Create the layout #this is the same for all 4 figures
layout = go.Layout(
    mapbox=dict(
        center=dict(lat=50.876, lon=4.70020),
        zoom=15,
        style='open-street-map'
    ),
    height=800,
    width=800,
    margin=dict(l=20, r=400, t=0, b=100)
)
# Create the figure
fig_laeq_daily = go.Figure(data=[data_trace], layout=layout)


## Lamax map daily ##
# Create the Scattermapbox trace
data_trace = go.Scattermapbox(
    lat=merged_daily['lat'],
    lon=merged_daily['lon'],
    mode='markers',
    marker=dict(
        size=merged_daily['standardized_lamax'],
        sizemode='diameter',
        sizeref=0.1,
        color='blue'
    ),
    customdata=merged_daily[['date', 'description', 'lamax', 'standardized_lamax']],
    hoverlabel=dict(namelength=0),
    hovertemplate='Date: %{customdata[0]}<br>'
                  'Location: %{customdata[1]}<br>'
                  'Noise level: %{customdata[2]:.2f} dB(A)<br>'
                  'Standardized noise level: %{customdata[3]:.2f} dB(A)'
)
fig_lamax_daily = go.Figure(data=[data_trace], layout=layout)


## Lamax map monthly ##
# Create the Scattermapbox trace
data_trace = go.Scattermapbox(
    lat=merged_daily['lat'],
    lon=merged_daily['lon'],
    mode='markers',
    marker=dict(
        size=merged_daily['standardized_lamax'],
        sizemode='diameter',
        sizeref=0.1,
        color='blue'
    ),
    customdata=merged_daily[['date', 'description', 'lamax', 'standardized_lamax']],
    hoverlabel=dict(namelength=0),
    hovertemplate='Month: %{customdata[0]}<br>'
                  'Location: %{customdata[1]}<br>'
                  'Noise level: %{customdata[2]:.2f} dB(A)<br>'
                  'Standardized noise level: %{customdata[3]:.2f} dB(A)'
)
fig_lamax_monthly = go.Figure(data=[data_trace], layout=layout)


## Laeq map monthly ##
data_trace = go.Scattermapbox(
    lat=merged_daily['lat'],
    lon=merged_daily['lon'],
    mode='markers',
    marker=dict(
        size=merged_daily['standardized_laeq'],
        sizemode='diameter',
        sizeref=0.1,
        color='blue'
    ),
    customdata=merged_daily[['date', 'description', 'laeq', 'standardized_laeq']],
    hoverlabel=dict(namelength=0),
    hovertemplate='Month: %{customdata[0]}<br>'
                  'Location: %{customdata[1]}<br>'
                  'Noise level: %{customdata[2]:.2f} dB(A)<br>'
                  'Standardized noise level: %{customdata[3]:.2f} dB(A)'
)
fig_laeq_monthly = go.Figure(data=[data_trace], layout=layout)

#style = {'width': '100%'}

layout = html.Div([
    html.H1(children='Noise map with sound monitor locations - TEST'),
    dcc.Dropdown(
        id="selected-map2",
        options=[
            {'label': 'Lamax', 'value': 'Lamax'},
            {'label': 'Laeq', 'value': 'Laeq'}
        ],
        value='Lamax',
        style={'width': '200px'}
    ),
    dcc.RadioItems(
    id="selected-period2",
    options=[
        {'label': 'Daily', 'value': 'Daily'},
        {'label': 'Monthly', 'value': 'Monthly'}
    ],
    value='Daily',
    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
    style={'font-size': '20px'}    
    ),
    dcc.Slider(
    id='date-slider',
    min=0,
    max=len(merged_daily)-1,
    value=len(merged_daily)-1,
    marks={i: merged_daily['date'][i] for i in range(len(merged_daily))},
    step=None
    ),
    dcc.Slider(
    id='month-slider',
    min=0,
    max=len(merged_monthly)-1,
    value=len(merged_monthly)-1,
    marks={i: merged_monthly['date'][i] for i in range(len(merged_monthly))},
    step=None
),
    dcc.Graph(id="noise-map2", style={'width': '50%', 'height': '80vh', 'margin': 'auto'})  
], 
style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})


@callback(
    Output("noise-map2", "figure"),
    [Input("selected-map2", "value"),
     Input("selected-period2", "value"),
     Input("date-slider", "value"),
     Input("month-slider", "value")]
)


def update_map(selected_map, selected_period, slider_value, month_slider_value):
    if selected_period == "Daily":
        if selected_map == "Lamax":
            fig = fig_lamax_daily
        else:
            fig = fig_laeq_daily
        fig.update_traces(selectedpoints=slider_value)
        #slider_style = {'display': 'none'} if selected_period == 'Monthly' else {'display': 'block'}
        fig.update_layout(updatemenus=[dict(buttons=[dict(args=[{"visible": True}], label="Play", method="animate")],
                                            direction="left", pad={"r": 10, "t": 10},
                                            showactive=False, x=0.1, xanchor="right", y=1.1, yanchor="top")],
                          sliders=[dict(steps=[], active=0, currentvalue={"prefix": "Date: "}
                                        )])
    else:
        if selected_map == "Lamax":
            fig = fig_lamax_monthly
        else:
            fig = fig_laeq_monthly
        fig.update_traces(selectedpoints=month_slider_value)
        fig.update_layout(sliders=[dict(steps=[], active=0, currentvalue={"prefix": "Month: "}
                                        )])
    return fig
