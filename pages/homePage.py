import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import numpy as np

dash.register_page(__name__, path='/')

#data_noise = pd.read_csv("Data/daily_noisedata_2022.csv")
data_noise_hour = pd.read_csv("Data for visualization/hourly_noisedata_2022.csv")

##########################
#noisiest location

average_lamax_per_location = data_noise_hour.groupby('description')['lamax'].mean()

location_with_highest_average = average_lamax_per_location.idxmax()
highest_average_value = average_lamax_per_location.max()

location_with_highest_average = location_with_highest_average.split(":")[-1].strip()


########################################
#noise time series

#data_noise_hour = pd.read_csv("Data/hourly_noisedata_2022.csv")

chose_location_timeseries = "MP 03: Naamsestraat 62 Taste"

data_Namen = data_noise_hour[data_noise_hour["description"]==chose_location_timeseries]


time = np.array(range(len(data_Namen)))

# Create a line plot using Plotly
fig_timeseries = go.Figure(data=go.Scatter(x=time, y=data_Namen["laeq"], mode='lines'))

# Customize the plot layout
fig_timeseries.update_layout(
    #title="Noise Levels Over Time - MP 03: Naamsestraat 62 Taste",
    #xaxis_title="Time",
    #yaxis_title="Laeq",
    margin=dict(l=0, r=0, t=0, b=0),
    plot_bgcolor='rgba(0, 0, 0, 0)',
    #width = 1200,
    #height = 150
)

##############################################
#polar plot

#different locations

# Extract the unique locations from the "description" column
locations = sorted(data_noise_hour["description"].unique())
#sorted to get in alphabetical order

number_locations = len(locations)
angle = 360/number_locations
# Create an array from 0 to 360 with steps of 45
angles = np.arange(0, 360, angle) #360 not included

# Compute the average "laeq" for each location
average_laeq = data_noise_hour.groupby("description")["laeq"].mean()
average_lamax = data_noise_hour.groupby("description")["lamax"].mean()


# Create a new dataframe by combining the average values
average_noise_per_location = pd.DataFrame({'Average laeq': average_laeq, 'Average lamax': average_lamax})

# Add the "description" as a column
average_noise_per_location['description'] = average_noise_per_location.index

# Remove the portion before ":" or "-" symbol, including any preceding numbers
average_noise_per_location['description'] = average_noise_per_location['description'].str.replace('.*?(?!(\d|$))[:|-]', '', regex=True)
#using a negative lookhead to keep the string if "\d" removes the complete string

average_noise_per_location['description'] = average_noise_per_location['description'].str.replace('.*?(?!\d{2,}$)(\d{1,2})', '', regex=True)

# Remove the portion before the digit or two digits, including the digit(s), except if it removes the complete string
#average_noise_per_location['description'] = average_noise_per_location['description'].apply(lambda x: np.nan if x == x.replace(x, '') else x.replace('.*?(?!\d{2,}$)(\d{1,2})', '', regex=True))

# Reset the index
average_noise_per_location.reset_index(drop=True, inplace=True)

# Remove the text "KU Leuven" if it is present
average_noise_per_location['description'] = average_noise_per_location['description'].str.replace('KU Leuven', '', regex=False)
#exception that I cannot fix with code
average_noise_per_location.loc[6, 'description'] = "Naamsestraat 81"

radius = 4.5

max_leaq_avg = average_laeq.max()
max_lamax_avg = average_lamax.max()

average_noise_per_location["radius"] = np.power(10,average_noise_per_location["Average laeq"]/10)/np.power(10,max_leaq_avg/10)*radius
average_noise_per_location["angle"] = np.power(10,average_noise_per_location["Average lamax"]/10)/np.power(10,max_lamax_avg/10)*angle

# Modify the ticktext for the fifth label
average_noise_per_location.loc[4,"description"] = "Kapel"

fig_polar_noise = go.Figure(go.Barpolar(
    r=average_noise_per_location["radius"],
    theta=angles,
    width=average_noise_per_location["angle"],
    marker_color=["#e86c8a", '#eb7d98',  '#e65b7d', '#e34a6f', '#f09fb3', '#ee8ea5', '#f3b0c0', '#f5c1ce'], #Maxim - Xior - Taste - His&Hears - Kapel - La Filosovia - Naamse - Vrijthof
    marker_line_color="black",
    marker_line_width=1,
    opacity=1,
    customdata=average_noise_per_location[["Average laeq", "Average lamax"]],
    hovertemplate="Average noise: %{customdata[0]:.2f} dB(A)<br>Maximal noise: %{customdata[1]:.2f} dB(A)<extra></extra>"
))

fig_polar_noise.update_layout(
    #margin=dict(l=50, r=50, t=20, b=20),  # Set margins to 0
    margin=dict(l=50, r=50, t=20, b=20),
    polar = dict(
        radialaxis = dict(range=[0, 5], showticklabels=False, ticks='', showline=False),
        angularaxis=dict(
            tickmode='array',
            tickvals=angles,
            ticktext=average_noise_per_location["description"],
            showticklabels=True, #True to see the labels of the locations
            tickfont = dict(color='white'),
            ticks=''
        )
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

#########################################################################################################"


weather_data = pd.read_csv("Data for visualization/daily_weatherdata_2022.csv", header = 0, sep=',')
cutoff_rain_day = 0.0002
weather_data["bool_rainday"] = weather_data["LC_DAILYRAIN"] > cutoff_rain_day
data_month = pd.read_csv('Data for visualization/monthly_weatherdata_2022.csv')


# Define the months and maximum days
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
max_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


import plotly.graph_objects as go
import numpy as np

# Filter the weather data for the month of January
january_data = weather_data[weather_data["Month"] == 1]

# Create an empty matrix to store the rain data
matrix = np.zeros((1, max_days[0]))

# Iterate over each day in January
for day in range(1, max_days[0] + 1):
    is_rainy = january_data[january_data["Day"] == day]["bool_rainday"].values[0]
    matrix[0, day - 1] = 1 if is_rainy else 0


# Create the heatmap figure
fig = go.Figure(data=go.Heatmap(z=matrix, colorscale=[[0, 'red'], [1, 'blue']],
                               x=list(range(1, max_days[0] + 1)),# y=["January"],
                               showscale=False,xgap=1))

# Set the layout for the heatmap
fig.update_layout(#title="Rain in January",
                  xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                  yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                             range=[-0.5,0.5]),
                  height=10,
                  margin=dict(l=0, r=0, t=0, b=0)  # Set the margins to 0 to remove padding
)


# Add 12 sub divs inside the central div
sub_divs = []

for i in range(12):

    #figure
    data_specific_month = weather_data[weather_data["Month"] == i+1]

    # Create an empty matrix to store the rain data
    matrix = np.zeros((1, max_days[i]))

    # Iterate over each day in January
    for day in range(1, max_days[i] + 1):
        is_rainy = data_specific_month[data_specific_month["Day"] == day]["bool_rainday"].values[0]
        matrix[0, day - 1] = 1 if is_rainy else 0

    color_zero = "rgba(158, 46, 61, 1.0)"
    color_one = "rgba(47, 119, 177, 1.0)"
    #handle extreme cases where all dry or wet
    if np.all(matrix == 1):
        color_zero = "rgba(47, 119, 177, 1.0)"
    elif np.all(matrix == 1):
        color_one = "rgba(158, 46, 61, 1.0)"

    # Create the heatmap figure
    fig = go.Figure(data=go.Heatmap(z=matrix, colorscale=[[0, color_zero], [1, color_one]],
                                x=list(range(1, max_days[i] + 1)),# y=["January"],
                                showscale=False,xgap=1))

    # Set the layout for the heatmap
    fig.update_layout(#title="Rain in January",
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                                range=[-0.5,0.5]),
                    height=10,
                    margin=dict(l=0, r=0, t=0, b=0)  # Set the margins to 0 to remove padding
    )


    temp_avg_month = round(data_month[data_month['Month']==i+1]["LC_TEMP_QCL3"],1).values[0]
    wind_avg_month = round(data_month[data_month['Month']==i+1]["LC_WINDSPEED"],2).values[0]
    sub_div = html.Div(
        style={'width': '100%', 'height': '50px', 'margin': '0px','display': 'flex', 'align-items': 'center', 'justify-content': 'center'}, #500px
        children=[
            html.Div(
                style={'width': '20%', 'height': '50px',  'margin': '0px','display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                children=[html.P(f"{months[i]}",style={"margin":"0"}),]),
            html.Div(
                style={'width': '10%', 'height': '50px', 'margin': '0px','display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                children=[html.P(f"{temp_avg_month}",style={"margin":"0"}),]),
            
            html.Div(
                style={'width': '60%'},
                children=[
                    dcc.Graph(figure=fig, style={'max-width': '100%'})
                ]
            ),

            html.Div(
                style={'width': '10%', 'height': '50px', 'margin': '0px','display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                children=[html.P(f'{wind_avg_month}',style={"margin":"0"}),]),
        ]
    )
    sub_divs.append(sub_div)

# Create a Plotly figure with the desired width and height
figure_width = 250
figure_height = 250

# Create a compass figure
fig_windDir = go.Figure(layout=dict(width=250, height=250))

# Add thin black lines for main wind directions
directions = ['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE']
for angle in range(0, 360, 45):
    fig_windDir.add_trace(go.Scatterpolar(
        r=[0, 1],
        theta=[angle, angle],
        mode='lines',
        line=dict(color='black', width=1, shape='linear'),
        hoverinfo='skip',
        showlegend=False
    ))

# Add compass needle marker
fig_windDir.add_trace(go.Scatterpolar(
    r=[0, 1],
    theta=[135, 135],
    mode='lines',
    line=dict(color='red', width=3, shape='linear'),
    hoverinfo='skip'
))

# Add compass needle marker at the tip
fig_windDir.add_trace(go.Scatterpolar(
    r=[1],
    theta=[135],
    mode='markers',
    marker=dict(color = "red",symbol='triangle-sw', size=15),
    hoverinfo='skip'
))

# Customize the layout
fig_windDir.update_layout(
    #title = dict(text="Wind direction", x = 0.5, font=dict(size=14)),
    polar=dict(
        radialaxis=dict(visible=False),
        angularaxis=dict(
            visible=True,
            tickmode='array',
            rotation=90,
            tickvals=[0, 45, 90, 135, 180, 225, 270, 315],
            ticktext=directions,
            tickfont=dict(size=20, family='Arial Bold',color="white"),
            showline=False,
            showgrid=False
        )
    ),
    showlegend=False,
    margin=dict(t=25,b=25,l=0, r=0)  # Set margin to remove padding on the left and right sides
    ,
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Set the plot background color to transparent
    paper_bgcolor='rgba(0, 0, 0, 0)'  # Set the paper background color to transparent

)

# Add the Plotly figure to the right-hand side of the central div
windDir_div = html.Div(
    style={'width': f'{figure_width}px', 'height': f'{figure_height}px','margin-left':"10px"},
    title = "Dominant wind direction",
    children=[
        dcc.Graph(figure=fig_windDir)
    ]
)

#################################################################################################################"
#make the donut plot - noise events


# Load the data
data_noise = pd.read_csv('Data for visualization/combined_noise_event.csv', header=0, sep=',')

# Calculate the frequencies of each category in the 'noise_source' variable
category_counts = data_noise['noise_event_laeq_primary_detected_class'].value_counts()

# Sort the categories by frequency in descending order
sorted_categories = category_counts.index.tolist()

# Calculate the total number of categories
num_categories = len(category_counts)

# Calculate the opacity levels
opacity_levels = [i / (num_categories - 1) for i in range(num_categories)]

# Reverse the list to make the largest category have the strongest opacity
opacity_levels.reverse()  

# Create a list of colors with adjusted opacity
colors = [f"rgba(227, 74, 111, {opacity})" for opacity in opacity_levels]

# Create a donut plot with customized colors
fig_donut = go.Figure(data=[
    go.Pie(
        labels=category_counts.index,
        values=category_counts.values,
        hole=0.6,
        marker=dict(colors=colors),
        textfont=dict(color='white'),
        showlegend=False,
        hovertemplate='<b>Noise source</b>: %{label}<br>'
                      '<b>Count</b>: %{value}<br>'
                      '<b>Percentage</b>: %{percent:.1%}<extra></extra>'
    )
])

# Set the layout options for the donut plot
fig_donut.update_layout(
    title=go.layout.Title(
        text="Noise Events <br>Distribution",
        x=0.56,
        y=0.52,
        xanchor="center",
        yanchor="middle",
        font=dict(color="white", size = 14) 
    ),
    showlegend=False,
    legend_title="Noise Sources",
    #width=400,
    #height=400,
    margin=go.layout.Margin(
        l=20,
        r=20,
        b=20,
        t=20,
        pad=4
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

# Add a white circle to create the donut effect
fig_donut.add_shape(
    type="circle",
    xref="paper",
    yref="paper",
    x0=0.35,
    y0=0.35,
    x1=0.65,
    y1=0.65,
    line_color="rgba(0,0,0,0)",
    fillcolor="rgba(0,0,0,0)",
)

#################################################################################################""
#html layout and css


layout = html.Div(
    style={
        'display': 'flex',
        'height': '100vh',
        'flex-direction': 'column', #add divs below each other
    },
    children=[
        html.Div(
            style={'width': '100%', 'height': '120px', 'padding': '0px','display':'flex'}, 
            children=[
                html.Div(
                    style={'flex': '1', 'padding-left': '2%', 'padding-right': '2%', 
                        'box-sizing': 'border-box',
                           }, 
                    children=[
                        html.Div(
                            style={'height':'100%','background-color': 'rgba(34, 49, 100, 0.89)', 'border': '1px solid white', 'padding': '0px','border-radius':'0.25rem',
                        'box-sizing': 'border-box'}, 
                            children=[
                                html.Div(
                                    style={'height':'100%','padding-left':'10%','padding-right':'0px','padding-top':'0px','padding-bottom':'0px'},
                                    children=[
                                        html.H2("8",style={'margin':'5% 0 0 0','font-size':'3vw'}),
                                        html.P("Locations",style={'margin':'2% 0 0 0'})
                                    ])
                            ]
                        )
                    ]
                ),  # Child 1
                html.Div(
                    style={'flex': '1', 'padding-left': '2%', 'padding-right': '2%',
                        'box-sizing': 'border-box',
                           },
                    children=[
                        html.Div(
                            style={'height':'100%','background-color': 'rgba(34, 49, 100, 0.89)', 'border': '1px solid white', 'padding': '0px','border-radius':'0.25rem',
                        'box-sizing': 'border-box'},
                            children=[
                                html.Div(
                                    style={'height':'100%','padding-left':'10%','padding-right':'0px','padding-top':'0px','padding-bottom':'0px'},
                                    children=[
                                        html.H2("His & Hears",style={'margin':'5% 0 0 0','font-size':'3vw'}),
                                        html.P("Noisiest location",style={'margin':'2% 0 0 0'})
                                    ])
                            ]
                        )
                    ]
                ),  # Child 2
                html.Div(
                    style={'flex': '1', 'padding-left': '2%', 'padding-right': '2%',
                        'box-sizing': 'border-box',
                           },
                    children=[
                        html.Div(
                            style={'height':'100%','background-color': 'rgba(34, 49, 100, 0.89)', 'border': '1px solid white', 'padding': '0px','border-radius':'0.25rem',
                        'box-sizing': 'border-box'},
                            children=[
                                html.Div(
                                    style={'height':'100%','padding-left':'10%','padding-right':'0px','padding-top':'0px','padding-bottom':'0px'},
                                    children=[
                                        html.H2("86.9 dB(A)",style={'margin':'5% 0 0 0','font-size':'3vw'}),
                                        html.P("Peak noise",style={'margin':'2% 0 0 0'})
                                    ])
                            ]
                        )
                    ]
                ),  # Child 3
                html.Div(
                    style={'flex': '1', 'padding-left': '2%', 'padding-right': '2%',
                        'box-sizing': 'border-box',
                           },
                    children=[
                        html.Div(
                            style={'height':'100%','background-color': 'rgba(34, 49, 100, 0.89)', 'border': '1px solid white', 'padding': '0px','border-radius':'0.25rem',
                        'box-sizing': 'border-box'},
                            children=[
                                html.Div(
                                    style={'height':'100%','padding-left':'10%','padding-right':'0px','padding-top':'0px','padding-bottom':'0px'},
                                    children=[
                                        html.H2("October",style={'margin':'5% 0 0 0','font-size':'3vw'}),
                                        html.P("Noisiest month",style={'margin':'2% 0 0 0'})
                                    ])
                            ]
                        )
                    ]
                ),  # Child 4
            ],
        ),
        html.Div(
            style={'width': '100%', 'height': '250px', 'border': '1px solid rgba(0, 0, 0, 0)', 'padding': '0px','margin-top':"20px", 'margin-left':"20px", 'margin-right':"20px", 'display': 'grid', 'grid-template-columns': '3fr 4fr 3fr', 'background-color': 'rgba(0,0,0,0)'},
            children=[
                html.Div(
                    style={'border': '1px solid rgba(0, 0, 0, 0)', 'box-sizing': 'border-box', 'background-color': 'rgba(0,0,0,0)'},
                    children=[
                        dcc.Graph(
                            id='plot-polar-noise-location',
                            figure=fig_polar_noise,
                            style={'width': '100%', 'height': '100%', 'background-color': 'rgba(0,0,0,0)'}
                        )
                    ],
                ),
                
                html.Div(style={'border': '1px solid rgba(0, 0, 0, 0)', 'box-sizing': 'border-box'},
                         children=[
                             html.Div(
                                style={'width': '100%', 'height': '250px', 'border': '1px solid rgba(0, 0, 0, 0)', 'padding': '0px'},
                                title="Average temperature, rainy days and average windspeed per month",
                                children=[
                                    html.Div(
                                        style={"position": "sticky", 'width': '100%', 'height': '35px', 'margin': '0px', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                                        children=[
                                            html.Div(
                                                style={'width': '20%', 'height': '35px', 'margin': '0px', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                                                children=[html.P("Month",style={"margin":"0"})],
                                            ),
                                            html.Div(
                                                style={'width': '10%', 'height': '35px', 'margin': '0px', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                                                children=[html.P("Temp",style={"margin":"0"})],
                                            ),
                                            html.Div(
                                                style={'width': '55%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                                                children=[
                                                    html.P("Rainy days",style={"margin":"0"})
                                                ],
                                            ),
                                            html.Div( #55 and 15 to make wind align with the numbers
                                                style={'width': '15%', 'height': '35px', 'margin': '0px', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                                                children=[html.P("Wind",style={"margin":"0"})],
                                            ),
                                        ],
                                    ),
                                    # Sub divs
                                    html.Div(
                                        style={'width': '100%', 'height': '215px', 'overflow': 'auto', 'overflow-x': 'hidden'},
                                        children=sub_divs
                                    ),
                                ],
                            ),
                         ]),  # Second div (40% width)
                html.Div(
                    style={'border': '1px solid rgba(0, 0, 0, 0)', 'box-sizing': 'border-box', 'margin-right':"40px", 'background-color': 'rgba(0,0,0,0)'},
                    children=[
                        dcc.Graph(
                            id='plot-donut-noise-events',
                            figure=fig_donut,
                            style={'width': '100%', 'height': '100%', 'background-color': 'rgba(0,0,0,0)'}
                        )
                    ],
                ),  # Third div (30% width)
                ]
            )
        ]
    )