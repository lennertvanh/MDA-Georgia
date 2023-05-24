import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

dash.register_page(__name__)

####################################################################################
## Data ##
daily_noise = pd.read_csv("Data/daily_noisedata_2022.csv")


######################################################################################"
#gps data"
# Create dataframe with GPS coordinates
gps_data = {
    'description': ['MP 01: Naamsestraat 35  Maxim', 'MP 02: Naamsestraat 57 Xior', 'MP 03: Naamsestraat 62 Taste', 'MP 04: His & Hears', 'MP 05: Calvariekapel KU Leuven', 'MP 06: Parkstraat 2 La Filosovia', 'MP 07: Naamsestraat 81', 'MP08bis - Vrijthof'],
    'lat': [50.877121, 50.87650, 50.87590, 50.875237, 50.87452, 50.874078, 50.873808, 50.87873],
    'lon': [4.700708, 4.700632, 4.700262, 4.700071, 4.69985, 4.70005, 4.700007, 4.70115]
}
gps_df = pd.DataFrame(gps_data)

######################################################################################
# Merging noise data with GPS coordinates
merged_daily = pd.merge(daily_noise, gps_df, on='description', how='left')
#merged_monthly = pd.merge(monthly_noise, gps_df, on='description', how='left')

######################################################################################
#setup arrays for months
months_for_cum_months = [0,31,28,31,30,31,30,31,31,30,31,30,31]
cumulative_months = np.cumsum(months_for_cum_months).tolist()


######################################################################################
#cumulative day
merged_daily["day_cum"] = merged_daily.apply(lambda row: cumulative_months[row["month"]-1] + row["day"], axis=1)


######################################################################################
# Group the data by 'day_cum' and apply the scaler separately for each group
max_laeq = merged_daily["laeq"].max()
min_laeq = merged_daily["laeq"].min()

start_size = 0.3 #minimum size
step_size = 0.7 #maximum size of 1 (0.3+0.7)

def divide_by_max(x):
    #max_value = x.max()#for each column separately: not good all the circles more or less same size
    return x / max_laeq

def myMapping(x):
    return start_size + step_size*(x-min_laeq)/(max_laeq-min_laeq)

merged_daily['laeq_std'] = merged_daily.groupby('day_cum')['laeq'].transform(myMapping)

######################################################################################
# Group the data by 'day_cum' and apply the scaler separately for each group
#same for lamax
max_lamax = merged_daily["lamax"].max()
min_lamax = merged_daily["lamax"].min()

start_size = 0.3 #minimum size
step_size = 0.7 #maximum size of 1 (0.3+0.7)

def myMapping(x):
    return start_size + step_size*(x-min_lamax)/(max_lamax-min_lamax)

merged_daily['lamax_std'] = merged_daily.groupby('day_cum')['lamax'].transform(myMapping)

######################################################################################

## Laeq map daily ##
# Create the Scattermapbox trace

filtered_data = merged_daily[merged_daily['day_cum'] == 90]

data_trace = go.Scattermapbox(
    lat=filtered_data['lat'],
    lon=filtered_data['lon'],
    mode='markers',
    marker=dict(
        size=filtered_data['laeq_std'],
        sizemode='diameter',
        sizeref=0.03,
        color='blue'
    ),
    customdata=filtered_data[['description', 'laeq']],
    hoverlabel=dict(namelength=0),
    hovertemplate='Location: %{customdata[0]}<br>'
                  'Noise level: %{customdata[1]:.2f} dB(A)<br>'
)
# Create the layout #this is the same for all 4 figures
layout_fig_map = go.Layout(
    mapbox=dict(
        center=dict(lat=50.876, lon=4.70020),
        zoom=15,
        style='open-street-map'
    ),
    #height=400,
    #width=200,
    margin=dict(l=0, r=0, t=0, b=0)
)
# Create the figure
fig_laeq_daily = go.Figure(data=[data_trace], layout=layout_fig_map)

######################################################################################
# Define the marks for the slider
marks = {day: str(day) for day in range(1, 366)}

# Create the slider component
slider = dcc.Slider(
    id='daily-slider',
    min=1,
    max=365,
    value=1,
    #marks=marks,
    step=None,  # Set step=None to allow only discrete values
)

######################################################################################


def convert_day_to_date(day):
    # Define the start date for the year
    start_date = datetime(2022, 1, 1)
    
    # Add the number of days to the start date
    target_date = start_date + timedelta(days=day - 1)
    
    # Format the date as desired (e.g., "5 March 2022")
    formatted_date = target_date.strftime("%d %B %Y")
    
    return formatted_date

# Example usage
#day = 365
#formatted_date = convert_day_to_date(day)

######################################################################################

# Update the layout with the clicked information
layout = html.Div(
    children=[
        html.Div(style={'flex': '15%'}),
        html.Div(
            children=[
                dcc.Graph(
                    id='map-id',
                    figure=fig_laeq_daily,
                    style={'width': '100%', 'height': '100%'},
                    clickData={'points': [{'customdata': ['Location', 0]}]}
                ),
                html.Div(id='clicked-data')  # Add this line to include the Div element for displaying click data
            ],
            style={'flex': '35%'}
        ),
        html.Div(children = [
                    html.Label('Select a day:'),
                    slider,
                    html.Div(
                        id='text-selected-day',
                        children=convert_day_to_date(1),
                        style={'margin': '10px'}
                    ),
                    html.Label('Select between laeq and lamax:'),
                    dcc.RadioItems(
                        id='radio-item-laeq-lamax-id',
                        options=[
                            {'label': 'laeq', 'value': 'option-laeq'},
                            {'label': 'lamax', 'value': 'option-lamax'},
                        ],
                        value='option-laeq',
                        labelStyle={'display': 'block'}  # Optional styling for the labels
        ),

        ], style={'flex': '35%','margin':'10px'}),
        html.Div(style={'flex': '15%'})
    ],
    style={'display': 'flex', 'height': '450px', 'width': '100%'}
)


######################################################################################
@callback(
    [Output('map-id', 'figure'), Output('text-selected-day', 'children'), Output('clicked-data', 'children')],
    [Input('daily-slider', 'value'), Input('radio-item-laeq-lamax-id', 'value'), Input('map-id', 'clickData')],
)

######################################################################################
def update_marker_size(selected_day, selected_data, click_data):
    filtered_data = merged_daily[merged_daily['day_cum'] == selected_day]

    if selected_data == "option-laeq":
        fig_laeq_daily.data[0].lat = filtered_data['lat']
        fig_laeq_daily.data[0].lon = filtered_data['lon']
        fig_laeq_daily.data[0].marker.size = filtered_data['laeq_std']

        # Convert the selected day to a formatted date string
        formatted_date = convert_day_to_date(selected_day)

        # Update the hovertemplate and customdata
        fig_laeq_daily.data[0].customdata = filtered_data[['description', 'laeq']]
        fig_laeq_daily.data[0].hovertemplate = 'Location: %{customdata[0]}<br>' \
                                               'Noise level: %{customdata[1]:.2f} dB(A)<br>'
    elif selected_data == "option-lamax":
        fig_laeq_daily.data[0].lat = filtered_data['lat']
        fig_laeq_daily.data[0].lon = filtered_data['lon']
        fig_laeq_daily.data[0].marker.size = filtered_data['lamax_std']

        # Convert the selected day to a formatted date string
        formatted_date = convert_day_to_date(selected_day)

        # Update the hovertemplate and customdata
        fig_laeq_daily.data[0].customdata = filtered_data[['description', 'lamax']]
        fig_laeq_daily.data[0].hovertemplate = 'Location: %{customdata[0]}<br>' \
                                               'Noise level: %{customdata[1]:.2f} dB(A)<br>'

    if click_data is not None:
        location = click_data['points'][0]['customdata'][0]
        noise_level = click_data['points'][0]['customdata'][1]
        clicked_text = html.Div(
            children=[
                html.Label('Clicked Point:'),
                html.P(f'Location: {location}'),
                html.P(f'Noise Level: {noise_level:.2f} dB(A)')
            ],
            style={'margin': '10px'}
        )
    else:
        clicked_text = ''

    return fig_laeq_daily, formatted_date, clicked_text
