import dash
from dash import html, dcc, callback
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output  #if I want a slider, button, ...


dash.register_page(__name__)


############################### DATA PREPARATION #################################
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
#using a negative lookhead to keep the string if "\d" removes the complete string

hourly_mean_data['description'] = hourly_mean_data['description'].str.replace('.*?(?!\d{2,}$)(\d{1,2})', '', regex=True)

# Remove the text "KU Leuven" if it is present
hourly_mean_data['description'] = hourly_mean_data['description'].str.replace('KU Leuven', '', regex=False)

#exception that I cannot fix with code: empty ones should be Naamsestraat 81
hourly_mean_data.loc[hourly_mean_data['description'] == '', 'description'] = "Naamsestraat 81"


################### FIGURE 1 ###################
data_hour_23 = hourly_mean_data[hourly_mean_data['hour'] == 23]
data_hour_23_sorted = data_hour_23.sort_values('description')

# Create a new DataFrame with the first row duplicated(so that the line connecting the last and first point isn't thinner than the other ones)
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
    marker_line_width=2,
    marker_size=3,
    hoverlabel=dict(namelength=0),
    hovertemplate='Maximal noise: %{r:.2f} dB(A)' 
))

# Update the layout
fig1.update_layout(
    margin=dict(l=0, r=0, t=40, b=40),
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[35, 61],
            tickmode='array',
            tickvals=[35, 40, 45, 50, 55, 60],
            ticktext=['', '40', '', '50', '', '60'],
            gridcolor='lightgrey',
            gridwidth=0.01,
            tickfont=dict(size=10)
        ),
        angularaxis=dict(
            tickfont=dict(size=15)  # Increase the font size of the locations
        ),
        bgcolor='white'
    ),
    plot_bgcolor='white',
    showlegend=True
)


################### FIGURE 2 ###################
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
    opacity=0.8,
    marker_line_width=2,
    marker_size=3,
    hoverlabel=dict(namelength=0),
    hovertemplate='Maximal noise: %{r:.2f} dB(A)' 
))

# layout stays the same
fig2.update_layout(
    margin=dict(l=0, r=0, t=40, b=40),
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[35, 61],
            tickmode='array',
            tickvals=[35, 40, 45, 50, 55, 60],
            ticktext=['', '40', '', '50', '', '60'],
            gridcolor='lightgrey',
            gridwidth=0.01,
            tickfont=dict(size=10)
        ),
        angularaxis=dict(
            tickfont=dict(size=15)  # Increase the font size of the locations
        ),
        bgcolor='white'
    ),
    plot_bgcolor='white',
    showlegend=True
)



layout = html.Div([
    html.H1("How do nightly noise peaks vary across different locations in Leuven?"),
    dcc.RadioItems(
        options=[
            {'label': '23h', 'value': '23h'},
            {'label': '0h', 'value': '0h'}
        ],
        value='23h',
        id='hour-radioitems'
    ),
    html.Div(id="spiderplot-container")
])


@callback(
    Output("spiderplot-container", "children"),
    [Input("hour-radioitems", "value")]
)
def update_figure(selected_hour):
    if selected_hour == "23h":
        return dcc.Graph(figure=fig1)
    elif selected_hour == "0h":
        return dcc.Graph(figure=fig2)


