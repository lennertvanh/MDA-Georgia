#########################################################################################################
# PACKAGES

import dash
from dash import html, dcc, callback
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output  #if I want a slider, button, ...

dash.register_page(__name__)


#########################################################################################################
# DATA

# Load the data
data_noise_hour = pd.read_csv("Data for visualization/hourly_noisedata_2022.csv")

# List of hour values for the nighttime
night_hours = [23, 0, 1, 2, 3, 4, 5]

# Subset the data for nighttime hours
data_hour_night = data_noise_hour[data_noise_hour['hour'].isin(night_hours)]

# Drop the month, day, and date columns
data_hour_night = data_hour_night.drop(['month', 'day', 'date'], axis=1)

# Calculate the mean of the other columns for each combination of hour and description
hourly_mean_data = data_hour_night.groupby(['hour', 'description']).mean().reset_index()

# Remove the portion before ":" or "-" symbol, including any preceding numbers
hourly_mean_data['description'] = hourly_mean_data['description'].str.replace('.*?(?!(\d|$))[:|-]', '', regex=True)
hourly_mean_data['description'] = hourly_mean_data['description'].str.replace('.*?(?!\d{2,}$)(\d{1,2})', '', regex=True)

# Remove the text "KU Leuven" if it is present
hourly_mean_data['description'] = hourly_mean_data['description'].str.replace('KU Leuven', '', regex=False)

# Exception that can not be fixed with code: empty ones should be Naamsestraat 81
hourly_mean_data.loc[hourly_mean_data['description'] == '', 'description'] = "Naamsestraat 81"

# Remove spaces at begin and end
hourly_mean_data['description'] = [description.strip() for description in hourly_mean_data['description']]


#########################################################################################################
# VISUALIZATION

# Common layout for all figures
common_layout = {
    "margin": dict(l=100, r=100, t=40, b=40),
    "polar": dict(
        radialaxis=dict(
            visible=True,
            showline=False,  # Hide the line of the radial axis
            range=[35, 60],
            tickmode='array',
            tickvals=[35, 40, 45, 50, 55, 60],
            ticktext=['35', '', '45', '', '      55 dB(A)', ''], #extra spaces for 55 to push it more to the right
            gridcolor='rgba(255, 255, 255, 0.1)',
            gridwidth=0.01,
            tickfont=dict(size=10, color='white')
        ), 
        angularaxis=dict(
            tickfont=dict(size=15, color='white'),
            gridcolor='rgba(255, 255, 255, 0.1)',
            gridwidth=0.01
        ),
        bgcolor='rgba(0,0,0,0)',
    ),
    "plot_bgcolor": "rgba(34, 49, 100, 0.89)",    # Set the plot area background color with transparency
    "paper_bgcolor": "rgba(34, 49, 100, 0.89)"
}


# FIGURE 1

# Subset the data to only include hour 23 + sort them by location
data_hour_23 = hourly_mean_data[hourly_mean_data['hour'] == 23]
data_hour_23_sorted = data_hour_23.sort_values('description')

# Create a new DataFrame with the first row duplicated (so that the line connecting the last and first point isn't thinner than the other ones)
first_row = data_hour_23_sorted.iloc[[0]]
data_hour_23_sorted_closed = pd.concat([data_hour_23_sorted, first_row], ignore_index=True)

# Initialize the figure
fig1 = go.Figure()

# Make the spider plot
fig1.add_trace(go.Scatterpolar(
    r=data_hour_23_sorted_closed['lamax'],  # Use maximal noise
    theta=data_hour_23_sorted_closed['description'],
    fill='toself',
    name='23h',
    opacity=0.8,
    marker=dict(
        color='#e6af2e'  # Set the marker color to #eb862e
    ),
    marker_line_width=2,
    marker_size=3,
    hoverlabel=dict(namelength=0),
    hovertemplate='Maximal noise: %{r:.2f} dB(A)' 
))

# Update the layout
fig1.update_layout(common_layout)


# FIGURE 2

# Subset the data to only include hour 0 + sort them by location
data_hour_0 = hourly_mean_data[hourly_mean_data['hour'] == 0]
data_hour_0_sorted = data_hour_0.sort_values('description')

# Create a new DataFrame with the first row duplicated (so that the line connecting the last and first point isn't thinner than the other ones)
first_row = data_hour_0_sorted.iloc[[0]]
data_hour_0_sorted_closed = pd.concat([data_hour_0_sorted, first_row], ignore_index=True)

# Initialize the figure
fig2 = go.Figure()

fig2.add_trace(go.Scatterpolar(
    r=data_hour_0_sorted_closed['lamax'],  # Use maximal noise
    theta=data_hour_0_sorted_closed['description'],
    fill='toself',
    name='00h',
    marker=dict(
        color='#e6af2e'  
    ),
    opacity=0.8,
    marker_line_width=2,
    marker_size=3,
    hoverlabel=dict(namelength=0),
    hovertemplate='Maximal noise: %{r:.2f} dB(A)' 
))

# Set common lay-out
fig2.update_layout(common_layout)


# FIGURE 3

# Subset the data to only include hour 1 + sort them by location
data_hour_1 = hourly_mean_data[hourly_mean_data['hour'] == 1]
data_hour_1_sorted = data_hour_1.sort_values('description')

# Create a new DataFrame with the first row duplicated (so that the line connecting the last and first point isn't thinner than the other ones)
first_row = data_hour_1_sorted.iloc[[0]]
data_hour_1_sorted_closed = pd.concat([data_hour_1_sorted, first_row], ignore_index=True)

# Initialize the figure
fig3 = go.Figure()

fig3.add_trace(go.Scatterpolar(
    r=data_hour_1_sorted_closed['lamax'],  # Use maximal noise
    theta=data_hour_1_sorted_closed['description'],
    fill='toself',
    name='01h',
    marker=dict(
        color='#e6af2e' 
    ),
    opacity=0.8,
    marker_line_width=2,
    marker_size=3,
    hoverlabel=dict(namelength=0),
    hovertemplate='Maximal noise: %{r:.2f} dB(A)' 
))

# Set common lay-out
fig3.update_layout(common_layout)


# FIGURE 4

# Subset the data to only include hour 2 + sort them by location
data_hour_2 = hourly_mean_data[hourly_mean_data['hour'] == 2]
data_hour_2_sorted = data_hour_2.sort_values('description')

# Create a new DataFrame with the first row duplicated (so that the line connecting the last and first point isn't thinner than the other ones)
first_row = data_hour_2_sorted.iloc[[0]]
data_hour_2_sorted_closed = pd.concat([data_hour_2_sorted, first_row], ignore_index=True)

# Initialize the figure
fig4 = go.Figure()

fig4.add_trace(go.Scatterpolar(
    r=data_hour_2_sorted_closed['lamax'],  # Use maximal noise
    theta=data_hour_2_sorted_closed['description'],
    fill='toself',
    name='02h',
    marker=dict(
        color='#e6af2e'  
    ),
    opacity=0.8,
    marker_line_width=2,
    marker_size=3,
    hoverlabel=dict(namelength=0),
    hovertemplate='Maximal noise: %{r:.2f} dB(A)' 
))

# Set common lay-out
fig4.update_layout(common_layout)


# FIGURE 5

# Subset the data to only include hour 3 + sort them by location
data_hour_3 = hourly_mean_data[hourly_mean_data['hour'] == 3]
data_hour_3_sorted = data_hour_3.sort_values('description')

# Create a new DataFrame with the first row duplicated (so that the line connecting the last and first point isn't thinner than the other ones)
first_row = data_hour_3_sorted.iloc[[0]]
data_hour_3_sorted_closed = pd.concat([data_hour_3_sorted, first_row], ignore_index=True)

# Initialize the figure
fig5 = go.Figure()

fig5.add_trace(go.Scatterpolar(
    r=data_hour_3_sorted_closed['lamax'],  # Use maximal noise
    theta=data_hour_3_sorted_closed['description'],
    fill='toself',
    name='03h',
    marker=dict(
        color='#e6af2e'  
    ),
    opacity=0.8,
    marker_line_width=2,
    marker_size=3,
    hoverlabel=dict(namelength=0),
    hovertemplate='Maximal noise: %{r:.2f} dB(A)' 
))

# Set common lay-out
fig5.update_layout(common_layout)


# FIGURE 6

# Subset the data to only include hour 4 + sort them by location
data_hour_4 = hourly_mean_data[hourly_mean_data['hour'] == 4]
data_hour_4_sorted = data_hour_4.sort_values('description')

# Create a new DataFrame with the first row duplicated (so that the line connecting the last and first point isn't thinner than the other ones)
first_row = data_hour_4_sorted.iloc[[0]]
data_hour_4_sorted_closed = pd.concat([data_hour_4_sorted, first_row], ignore_index=True)

# Initialize the figure
fig6 = go.Figure()

fig6.add_trace(go.Scatterpolar(
    r=data_hour_4_sorted_closed['lamax'],  # Use maximal noise
    theta=data_hour_4_sorted_closed['description'],
    fill='toself',
    name='04h',
    marker=dict(
        color='#e6af2e'  
    ),
    opacity=0.8,
    marker_line_width=2,
    marker_size=3,
    hoverlabel=dict(namelength=0),
    hovertemplate='Maximal noise: %{r:.2f} dB(A)' 
))

# Set common lay-out
fig6.update_layout(common_layout)


# FIGURE 6

# Subset the data to only include hour 5 + sort them by location
data_hour_5 = hourly_mean_data[hourly_mean_data['hour'] == 5]
data_hour_5_sorted = data_hour_5.sort_values('description')

# Create a new DataFrame with the first row duplicated (so that the line connecting the last and first point isn't thinner than the other ones)
first_row = data_hour_5_sorted.iloc[[0]]
data_hour_5_sorted_closed = pd.concat([data_hour_5_sorted, first_row], ignore_index=True)

# Initialize the figure
fig7 = go.Figure()

fig7.add_trace(go.Scatterpolar(
    r=data_hour_5_sorted_closed['lamax'],  # Use maximal noise
    theta=data_hour_5_sorted_closed['description'],
    fill='toself',
    name='5h',
    marker=dict(
        color='#e6af2e' 
    ),
    opacity=0.8,
    marker_line_width=2,
    marker_size=3,
    hoverlabel=dict(namelength=0),
    hovertemplate='Maximal noise: %{r:.2f} dB(A)' 
))

# Set common lay-out
fig7.update_layout(common_layout)


#########################################################################################################
# PAGE LAYOUT

layout = html.Div([
    html.H2("How do nightly noise peaks vary across different locations in Leuven?"),
    html.Div(
        dcc.RadioItems( # Add radio buttons for each nightly hour
            options=[
                {'label': '23h', 'value': '23h'},
                {'label': '00h', 'value': '00h'},
                {'label': '01h', 'value': '01h'},
                {'label': '02h', 'value': '02h'},
                {'label': '03h', 'value': '03h'},
                {'label': '04h', 'value': '04h'},
                {'label': '05h', 'value': '05h'}
            ],
            value='23h', # default value 
            id='hour-radioitems',
            labelStyle={'display': 'inline-block'},
            style={'margin-left': 'auto', 'margin-right': 'auto', 'margin-bottom': '20px', 'margin-top': '20px', 'display': 'flex', 'justify-content': 'center'}
        ),
    ),
    html.Div(
        id="spiderplot-container")
])


#########################################################################################################
# CALLBACK UPDATE FIGURE (changes the displayed figure when a different radio button is selected)

@callback(
    Output("spiderplot-container", "children"),
    [Input("hour-radioitems", "value")]
)
def update_figure(selected_hour):
    if selected_hour == "23h":
        return dcc.Graph(figure=fig1)
    elif selected_hour == "00h":
        return dcc.Graph(figure=fig2)
    elif selected_hour == "01h":
        return dcc.Graph(figure=fig3)
    elif selected_hour == "02h":
        return dcc.Graph(figure=fig4)
    elif selected_hour == "03h":
        return dcc.Graph(figure=fig5)
    elif selected_hour == "04h":
        return dcc.Graph(figure=fig6)
    elif selected_hour == "05h":
        return dcc.Graph(figure=fig7)