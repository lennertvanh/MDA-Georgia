import dash
from dash import html, dcc, callback
import pandas as pd
import datetime
import plotly.graph_objects as go
from dash.dependencies import Input, Output  #if I want a slider, button, ...

# this is so my buttons work properly
app = dash.Dash(__name__)
app.register_page(__name__)


## DATA ##

noise_data = pd.read_csv("Data/hourly_noisedata_2022.csv")

# Should we take the mean over all locations first? Or make it such that you can select the locations?
# take the mean value across all locations
noise_per_hour = noise_data.drop(columns='description', axis=1)
noise_per_hour = noise_per_hour.groupby(['month', 'day', 'hour']).mean()
noise_per_hour = noise_per_hour.reset_index()

noise_per_hour['wk_day'] = None
for index, row in noise_per_hour.iterrows():
    hour = row['hour']
    day = row['day']
    month = row['month']
    dt = datetime.datetime(2022, month, day, hour)
    # Get the abbreviated weekday name (e.g., Mon, Tue, Wed) and assign it to the 'wk_day' column
    noise_per_hour.at[index, 'wk_day'] = dt.strftime("%a")

weekday_order = ['Sun', 'Sat', 'Fri', 'Thu', 'Wed', 'Tue', 'Mon']


## figures ##

# FIGURE 1
fig1 = go.Figure()

fig1.add_trace(go.Heatmap(
    x=noise_per_hour['hour'],
    y=noise_per_hour['wk_day'],
    z=noise_per_hour['laeq'], # NOTE: standardizing the data gives the exact same heatmap so no use in doing this
    colorscale='Reds',  
    hovertemplate='Hour: %{x}<br>Weekday: %{y}<br>Sound level: %{z:.2f} dB(A)',
    hoverlabel=dict(namelength=0),
    ygap=1,  
    yperiodalignment='middle',  
))

fig1.update_layout(
    title={
        'text': 'Average noise in Leuven throughout the day',
        'x': 0.5,  
        'xanchor': 'center',  
    },
    xaxis=dict(
        title='Time of day',
        tickvals=[0, 6, 12, 18, 23],  
    ),
    yaxis=dict(
        title='Weekday',
        categoryorder='array',
        categoryarray=weekday_order,
    ),
)

# FIGURE 2

# Select rows where the hour is in the desired range
nightly_noise = noise_per_hour[noise_per_hour['hour'].isin([0, 1, 2, 3, 4, 5, 23])].copy()
nightly_noise.reset_index(drop=True, inplace=True)
nightly_noise.loc[nightly_noise['hour'] == 23, 'hour'] = -1 # to be able to plot 23h on the left

fig2 = go.Figure()

fig2.add_trace(go.Heatmap(
    x=nightly_noise['hour'],
    y=nightly_noise['wk_day'],
    z=nightly_noise['laeq'], 
    colorscale='Reds',  
    hovertemplate='Hour: %{x}<br>Weekday: %{y}<br>Sound level: %{z:.2f} dB(A)',
    hoverlabel=dict(namelength=0),
    ygap=1,  
    yperiodalignment='middle', 
))

fig2.update_layout(
    title={
        'text': 'Average noise in Leuven at night: Thursday = party day',
        'x': 0.5,  
        'xanchor': 'center',  
    },
    xaxis=dict(
        title='Time of day',
        categoryorder='array',
        categoryarray=[-1, 0, 1, 2, 3, 4, 5],
        tickmode='array',
        tickvals=[-1, 0, 1, 2, 3, 4, 5],
        ticktext=['23', '0', '1', '2', '3', '4', '5'],
        range=[-1.5, 5.5],
    ),
    yaxis=dict(
        title='Weekday',
        categoryorder='array',
        categoryarray=weekday_order,
    ),
)

# Annotate the box for Thursday at hour 4
fig2.update_layout(
    annotations=[
        dict(
            x=4,
            y=weekday_order.index('Thu'),
            text='<b>drunk students returning<br>to their dorm</b>',
            showarrow=False,
            font=dict(color='black', size=8),  
            bgcolor='rgba(255, 255, 0, 0)',  # transparent background
            bordercolor='rgba(255, 255, 0, 0)',  # transparent border
        )
    ]
)

layout = html.Div([
    html.H1("Heatmap of noise"),
    html.Button("Entire day", id="entire-day-button", n_clicks=0),
    html.Button("At night", id="at-night-button", n_clicks=0),
    html.Div(id="heatmap-container")
])

@app.callback(
    Output("heatmap-container", "children"),
    [Input("entire-day-button", "n_clicks"),
     Input("at-night-button", "n_clicks")]
)

def update_figure(entire_day_clicks, at_night_clicks):
    if entire_day_clicks > 0:
        return dcc.Graph(figure=fig1)
    elif at_night_clicks > 0:
        return dcc.Graph(figure=fig2)
    else:
        return dcc.Graph(figure=fig1)
