#########################################################################################################
# PACKAGES

import dash
from dash import html, dcc, callback,get_asset_url
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

dash.register_page(__name__)


#########################################################################################################
# DATA
daily_noise = pd.read_csv("Data for visualization/daily_noisedata_2022.csv")
daily_weather = pd.read_csv("Data for visualization/daily_weatherdata_2022.csv")

# Path images
image_rainy = "rainy-icon.jpg"
image_sunny = "sunny-day.jpg"
image_cloudly = "Cloudly.jpg"

# Create dataframe with GPS coordinates
gps_data = {
    'description': ['MP 01: Naamsestraat 35  Maxim', 'MP 02: Naamsestraat 57 Xior', 'MP 03: Naamsestraat 62 Taste', 'MP 04: His & Hears', 'MP 05: Calvariekapel KU Leuven', 'MP 06: Parkstraat 2 La Filosovia', 'MP 07: Naamsestraat 81', 'MP08bis - Vrijthof'],
    'lat': [50.877121, 50.87650, 50.87590, 50.875237, 50.87452, 50.874078, 50.873808, 50.87873],
    'lon': [4.700708, 4.700632, 4.700262, 4.700071, 4.69985, 4.70005, 4.700007, 4.70115]
}
gps_df = pd.DataFrame(gps_data)


# Merging noise data with GPS coordinates
merged_daily = pd.merge(daily_noise, gps_df, on='description', how='left')
#merged_monthly = pd.merge(monthly_noise, gps_df, on='description', how='left')

#setup arrays for months
months_for_cum_months = [0,31,28,31,30,31,30,31,31,30,31,30,31]
cumulative_months = np.cumsum(months_for_cum_months).tolist()

#cumulative day
merged_daily["day_cum"] = merged_daily.apply(lambda row: cumulative_months[row["month"]-1] + row["day"], axis=1)
daily_weather["day_cum"] = daily_weather.apply(lambda row: cumulative_months[np.int64(row["Month"])-1] + row["Day"], axis=1)

# MEAN SOUND LEVEL
# Group the data by 'day_cum' and apply the scaler separately for each group
max_laeq = merged_daily["laeq"].max()
min_laeq = merged_daily["laeq"].min()

# Create custom scaler/mapping for the sizes of the points on the map (proportional to sound level)
start_size = 0.3 #minimum size
step_size = 0.7 #maximum size of 1 (0.3+0.7)

def divide_by_max(x):
    #max_value = x.max() #for each column separately: not good all the circles more or less same size
    return x / max_laeq

def myMapping(x):
    return start_size + step_size*(x-min_laeq)/(max_laeq-min_laeq)

merged_daily['laeq_std'] = merged_daily.groupby('day_cum')['laeq'].transform(myMapping)

# Repeat steps for MAX SOUND LEVEL
max_lamax = merged_daily["lamax"].max()
min_lamax = merged_daily["lamax"].min()

# same start and step size
def myMapping(x):
    return start_size + step_size*(x-min_lamax)/(max_lamax-min_lamax)

merged_daily['lamax_std'] = merged_daily.groupby('day_cum')['lamax'].transform(myMapping)

# Change the locations names 
replacements = {
    'MP 01: Naamsestraat 35  Maxim': 'Maxim (Naamsestraat 35)',
    'MP 02: Naamsestraat 57 Xior': 'Xior (Naamsestraat 57)',
    'MP 03: Naamsestraat 62 Taste': 'Taste (Naamsestraat 62)',
    'MP 04: His & Hears': 'His & Hears',
    'MP 05: Calvariekapel KU Leuven': 'Calvariekapel KU Leuven',
    'MP 06: Parkstraat 2 La Filosovia': 'La Filosovia (Parkstraat 2)',
    'MP 07: Naamsestraat 81': 'Naamsestraat 81',
    'MP08bis - Vrijthof': 'Vrijthof (stadhuis Leuven)'
}
# Replace the values in the "description" column
merged_daily['description'] = merged_daily['description'].replace(replacements)

# Merge noise and weather data together in a final dataset
merged_data = pd.merge(merged_daily, daily_weather, on='day_cum', how='left')

# Function to convert the day (value on the slider) to a date
def convert_day_to_date(day):
    # Define the start date for the year
    start_date = datetime(2022, 1, 1)
    
    # Add the number of days to the start date
    target_date = start_date + timedelta(days=day - 1)
    
    # Format the date as desired (e.g., "5 March 2022")
    formatted_date = target_date.strftime("%d %B %Y")
    
    return formatted_date



#########################################################################################################
# VISUALIZATION

# Initialize filtered data
filtered_data = merged_data[merged_data['day_cum'] == 1] 

# Mean sound level (= the one when you enter the page)
# Create the Scattermapbox trace
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
    customdata=filtered_data[['description', 'laeq', 'LC_TEMP_QCL3']],
    hoverlabel=dict(namelength=0),
    hovertemplate='Location: %{customdata[0]}<br>'
                  'Noise level: %{customdata[1]:.2f} dB(A)<br>'
                  'Temperature: %{customdata[2]:.1f} °C<br>'
)

# Create the common layout
layout_fig_map = go.Layout(
    mapbox=dict(
        center=dict(lat=50.8762, lon=4.70020),
        zoom=15,
        style='open-street-map'
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

# Create the figure (= the one when you enter the page)
fig_laeq_daily = go.Figure(data=[data_trace], layout=layout_fig_map)



#########################################################################################################
# PAGE LAYOUT

# Create the slider component
slider = dcc.Slider(
    id='daily-slider',
    min=1,
    max=365,
    value=1,
    step=None,  # Set step=None to allow only discrete values
    className='slider-white',
)

# Initialize the selected location TEXT
last_selected_location = 'Please select a location'

# Update the layout with the clicked information
layout = html.Div(
    children=[
        html.Div(
            [
                html.H2("Noise map"),
                html.P("This map displays the different locations in Leuven for which the noise levels were measured. Some locations don't have any observations during certain months. The blue circles are proportional to the observed sound levels. A distinction is made between the average and maximal noise levels per day. The day can be chosen with the slider, it automatically updates the weather icon to showcase whether it was raining a lot, a little or if the sun was shining in Leuven that day. Moreover, clicking a point will display its location name, observed sound level and the temperature in Leuven for the particular day."),
            ],
            style={'margin-bottom': '20px'}
        ),
        html.Div(
            [
                html.Div(style={'flex': '15%'}),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='map-id',
                            figure=fig_laeq_daily,
                            style={'width': '100%', 'height': '100%'},
                            clickData={'points': [{'customdata': [last_selected_location, 0, 1]}]} 
                        ), 
                    ],
                    style={'flex': '35%', 'display': 'inline-block'}
                ),
                html.Div(
                    children=[
                        html.Label('Select a day:', style={'font-size': '20px'}),
                        slider,
                        html.Div(
                            id='text-selected-day',
                            children=convert_day_to_date(1),
                            style={'margin': '3px 10px 50px'}
                        ),
                        html.Label('Select between average and maximal noise level:', style={'font-size': '20px'}),
                        dcc.RadioItems(
                            id='radio-item-laeq-lamax-id',
                            options=[
                                {'label': 'Average noise level', 'value': 'option-laeq'},
                                {'label': 'Maximal noise level', 'value': 'option-lamax'},
                            ],
                            value='option-laeq',
                            labelStyle={'display': 'block'}
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    id='clicked-data',
                                    style={'margin': '50px 0px', "width": "65%", 'display': 'flex', 'justify-content': 'flex-start'}
                                ),
                                html.Div(id="image-container", style={"width": "25%", "max-height": "100%", 'margin': '100px 40px'})
                            ],
                            style={'display': 'flex'}
                        ),

                    ], style={'flex': '45%', 'margin': '30px', 'vertical-align': 'top', 'display': 'inline-block'}
                ),
                html.Div(style={'flex': '15%'})
            ],
            style={'display': 'flex', 'height': '450px', 'width': '100%'}
        )
    ]
)



#########################################################################################################
# CALLBACK UPDATE GRAPH

# Store the last selected slider value
last_slider_value = 1

# Callback function to update the entire page (graph, clicked info, weather icon)
@callback(
    [Output('map-id', 'figure'), Output('text-selected-day', 'children'), Output('clicked-data', 'children'), Output("image-container", "children")],
    [Input('daily-slider', 'value'), Input('radio-item-laeq-lamax-id', 'value'), Input('map-id', 'clickData')],
)
def update_page(selected_day, selected_data, click_data):
    global last_slider_value  # Declare the variable as global to modify it within the function
    last_slider_value = selected_day # Update the last_slider_value with the current selected_day

    filtered_data = merged_data[merged_data['day_cum'] == selected_day]

    selected_weather = daily_weather.loc[selected_day-1]

    #criterions can be changed later
    if(selected_weather["LC_DAILYRAIN"]>0.0002): #rainy day
        image_path = image_rainy
    elif(selected_weather["LC_TEMP_QCL3"]>15): #average temperature above 15°C and not rainy
        image_path = image_sunny
    elif(selected_weather["LC_DAILYRAIN"]>0.00002): #some rain and not "warm"
        image_path = image_cloudly
    else: #almost no rain and cold 
        image_path = image_sunny

    #if a point is selected (noiselevel higher than zero)
    if(click_data['points'][0]['customdata'][1]>0):
        click_data['points'][0]['customdata'][2] = selected_weather["LC_TEMP_QCL3"] #update the temperature with the temperature of the day

    if selected_data == "option-laeq":
        fig_laeq_daily.data[0].lat = filtered_data['lat']
        fig_laeq_daily.data[0].lon = filtered_data['lon']
        fig_laeq_daily.data[0].marker.size = filtered_data['laeq_std']
        fig_laeq_daily.data[0].marker.color = ['blue'] * len(filtered_data) #make them all blue

        # Convert the selected day to a formatted date string
        formatted_date = convert_day_to_date(selected_day)

        # Update the hovertemplate and customdata
        fig_laeq_daily.data[0].customdata = filtered_data[['description', 'laeq', 'LC_TEMP_QCL3']]
        fig_laeq_daily.data[0].hovertemplate = 'Location: %{customdata[0]}<br>' \
                                               'Noise level: %{customdata[1]:.2f} dB(A)<br>' \
                                               'Temperature: %{customdata[2]:.1f} °C<br>'
        
        location = click_data['points'][0]['customdata'][0]
        location_array = filtered_data['description'].values
        if(int(click_data['points'][0]['customdata'][1])>0 and location in location_array):
            click_data['points'][0]['customdata'][1] = filtered_data[filtered_data["description"]==location]["laeq"].values[0] #update the laeq
        elif(location not in location_array):
            click_data['points'][0]['customdata'][1] = 0
        
    elif selected_data == "option-lamax":
        fig_laeq_daily.data[0].lat = filtered_data['lat']
        fig_laeq_daily.data[0].lon = filtered_data['lon']
        fig_laeq_daily.data[0].marker.size = filtered_data['lamax_std']
        fig_laeq_daily.data[0].marker.color = ['blue'] * len(filtered_data) #make them all blue

        # Convert the selected day to a formatted date string
        formatted_date = convert_day_to_date(selected_day)

        # Update the hovertemplate and customdata
        fig_laeq_daily.data[0].customdata = filtered_data[['description', 'lamax', 'LC_TEMP_QCL3']]
        fig_laeq_daily.data[0].hovertemplate = 'Location: %{customdata[0]}<br>' \
                                               'Noise level: %{customdata[1]:.2f} dB(A)<br>' \
                                               'Temperature: %{customdata[2]:.1f} °C<br>'
        
        location = click_data['points'][0]['customdata'][0]
        location_array = filtered_data['description'].values
        if(int(click_data['points'][0]['customdata'][1])>0 and location in location_array):
            click_data['points'][0]['customdata'][1] = filtered_data[filtered_data["description"]==location]["lamax"].values[0] #update the laeq
        elif(location not in location_array):
            click_data['points'][0]['customdata'][1] = 0
        
    if click_data is not None:
        location = click_data['points'][0]['customdata'][0]
        noise_level = click_data['points'][0]['customdata'][1]
        temperature = click_data['points'][0]['customdata'][2]

        #if selected data, make the clicked location red
        #if a location is selected
        if(noise_level>0):
            #point_index = click_data['points'][0]['pointIndex']
            filtered_data.reset_index(drop=True, inplace=True)

            location_array = filtered_data['description'].values

            #if location exists at that time, sometimes location is not in the dataset
            if(location in location_array):
                
                point_index = filtered_data[filtered_data['description'] == location].index[0]

                # Convert the color attribute tuple to a list
                color_list = list(fig_laeq_daily.data[0].marker.color)

                # Modify the color attribute for the specific index to 'red'
                color_list[point_index] = 'red'

                # Convert the color list back to a tuple
                fig_laeq_daily.data[0].marker.color = tuple(color_list)


        clicked_text = html.Div(
            children=[
        html.Label('Clicked Point:', style={'font-size': '20px'}),
        html.P(children=[
            html.Strong('Location: '),
            location if isinstance(location, str) else '', 
            ], 
            style={'margin-left': '5px'} #need to add this to not have a very large indentation
        ),
        html.P(children=[
            html.Strong('Noise Level: '),
            f'{noise_level:.2f} dB(A)' if isinstance(noise_level, float) else '', #if no point (no sound level) is selected: empty string
            ], 
            style={'margin-left': '5px'}
        ),
        html.P(children=[
            html.Strong('Temperature: '),
            f'{temperature:.1f} °C' if isinstance(temperature, float) else '', #if no point is selected: empty string 
            ],
            style={'margin-left': '5px'}
        ),
    ]
)
        
    # Create an HTML component for displaying the image with specified source and styling
    image_html_comp = html.Img(src=dash.get_asset_url(image_path), style={"width": "100%", "max-height": "100%", "object-fit": "contain"})


    return fig_laeq_daily, formatted_date, clicked_text, image_html_comp 