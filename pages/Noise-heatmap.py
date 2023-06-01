#########################################################################################################
# PACKAGES

import dash
from dash import html, dcc, callback
import pandas as pd
import datetime
import plotly.graph_objects as go
from dash.dependencies import Input, Output  #if I want a slider, button, ...

dash.register_page(__name__)

#########################################################################################################
# DATA

noise_data = pd.read_csv("Data for visualization/hourly_noisedata_2022.csv")

# Take the mean value across all locations
noise_per_hour = noise_data.drop(columns=['description', 'date'], axis=1)
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


#########################################################################################################
# VISUALIZATION

# FIGURE 1
fig1 = go.Figure()

fig1.add_trace(go.Heatmap(
    x=noise_per_hour['hour'],
    y=noise_per_hour['wk_day'],
    z=noise_per_hour['laeq'], # NOTE: standardizing the data gives the exact same heatmap so no use in doing this
    colorscale='Reds',  
    hovertemplate='Hour: %{x}<br>Weekday: %{y}<br>Noise level: %{z:.2f} dB(A)',
    hoverlabel=dict(namelength=0),
    yperiodalignment='middle', 
    colorbar=dict(
        tickfont=dict(color='white')  
    )
))

fig1.update_layout(
    title={
        'text': 'Average noise in Leuven throughout the day',
        'x': 0.5,  
        'xanchor': 'center', 
        'font': {'color': 'white', 'size': 24}  
    },
    xaxis=dict(
        title='Time of day',
        tickvals=[0, 4, 8, 12, 16, 20, 23],
        title_font=dict(color="white", size =18),
        tickfont=dict(color="white"),
        gridcolor='rgba(0, 0, 0, 0)',  
        zeroline=False 
    ),
    yaxis=dict(
        title='Weekday',
        categoryorder='array',
        categoryarray=weekday_order,
        title_font=dict(color="white", size =18),
        tickfont=dict(color="white"),
        gridcolor='rgba(0, 0, 0, 0)',  
    ),
    plot_bgcolor='rgba(0,0,0,0)',  
    paper_bgcolor='rgba(0,0,0,0)',  
)

# Add annotations
fig1.add_annotation(
    xref='x',
    yref='y',
    x=21.5,
    y=weekday_order.index('Fri'),
    text='<b>students going home<br> for the weekend</b>',
    showarrow=True,
    arrowside='none',
    arrowcolor='white',
    ax=-110,
    ay=-175,
    font=dict(color='black', size=10),  
    bordercolor='black',  
    borderwidth=1, 
    bgcolor='white',  
    opacity=0.9  
)
fig1.add_annotation(
    xref='x',
    yref='y',
    x=21,
    y=weekday_order.index('Sun'),
    text='<b>students arriving in<br>Leuven for the school week</b>',
    showarrow=True,
    arrowside='none',
    arrowcolor='white',
    ax=-250,
    ay=-240,
    font=dict(color='black', size=10),  
    bordercolor='black',  
    borderwidth=1,  
    bgcolor='white', 
    opacity=0.9 
)
fig1.add_annotation(
    xref='x',
    yref='y',
    x=23,
    y=weekday_order.index('Sat'),
    text='<b>international students<br>on their way to parties</b>',
    showarrow=True,
    arrowside='none',
    arrowcolor='white',
    ax=-20,
    ay=-207.5,
    font=dict(color='black', size=10),  
    bordercolor='black',  
    borderwidth=1,  
    bgcolor='white', 
    opacity=0.9 
)
fig1.add_annotation(
    xref='x',
    yref='y',
    x=11.5,
    y=weekday_order.index('Sun'),
    text='<b>Sunday market</b>',
    showarrow=True,
    arrowside='none',
    arrowcolor='white',
    ax=-150,
    ay=-240,
    font=dict(color='black', size=10), 
    bordercolor='black',  
    borderwidth=1,  
    bgcolor='white',  
    opacity=0.9 
)
fig1.add_annotation(
    xref='x',
    yref='y',
    x=13.5,
    y=weekday_order.index('Fri'),
    text='<b>students going home<br> for the weekend</b>',
    showarrow=True,
    arrowside='none',
    arrowcolor='white',
    ax=-110,
    ay=-175,
    font=dict(color='black', size=10),  
    bordercolor='black',  
    borderwidth=1,  
    bgcolor='white',  
    opacity=0.9  
)

# FIGURE 2

# Select rows where the hour is in the desired range
nightly_noise = noise_per_hour[noise_per_hour['hour'].isin([0, 1, 2, 3, 4, 5])].copy()
nightly_noise.reset_index(drop=True, inplace=True)

fig2 = go.Figure()

fig2.add_trace(go.Heatmap(
    x=nightly_noise['hour'],
    y=nightly_noise['wk_day'],
    z=nightly_noise['laeq'], 
    colorscale='Reds',  
    hovertemplate='Hour: %{x}<br>Weekday: %{y}<br>Noise level: %{z:.2f} dB(A)',
    hoverlabel=dict(namelength=0),
    yperiodalignment='middle', 
    colorbar=dict(
        tickfont=dict(color='white')  
    )
))

fig2.update_layout(
    title={
        'text': 'Average noise in Leuven at night',
        'x': 0.5,  
        'xanchor': 'center',  
        'font': {'color': 'white', 'size' : 24}  
    },
    xaxis=dict(
        title='Time of day',
        categoryorder='array',
        categoryarray=[1, 2, 3, 4, 5],
        tickmode='array',
        tickvals=[0, 1, 2, 3, 4, 5],
        ticktext=['0', '1', '2', '3', '4', '5'],
        range=[-0.5, 5.5],
        title_font=dict(color="white", size =18),
        tickfont=dict(color="white"),
        gridcolor='rgba(0, 0, 0, 0)', 
        zeroline=False  
    ),
    yaxis=dict(
        title='Weekday',
        categoryorder='array',
        categoryarray=weekday_order,
        title_font=dict(color="white", size =18),
        tickfont=dict(color="white"),
        gridcolor='rgba(0, 0, 0, 0)',  
    ),
    plot_bgcolor='rgba(0,0,0,0)', 
    paper_bgcolor='rgba(0,0,0,0)',
)

# Annotatations
fig2.add_annotation(
    xref='x',
    yref='y',
    x=3.5,
    y=weekday_order.index('Thu'),
    text='<b>drunk students returning to<br> their dorm after partying</b>',
    showarrow=True,
    arrowhead=1,
    arrowcolor='white',
    arrowside='none',
    ax=30,
    ay=-140,
    font=dict(color='black', size=10),  
    bordercolor='black',  
    borderwidth=1,  
    bgcolor='white', 
    opacity=0.9  
)
fig2.add_annotation(
    xref='x',
    yref='y',
    x=0.5,
    y=weekday_order.index('Sat'),
    text='<b>internationals and high schoolers<br> on their way to parties</b>',
    showarrow=True,
    arrowhead=1,
    arrowcolor='white',
    arrowside='none',
    ax=100,
    ay=-205,
    font=dict(color='black', size=10),  
    bordercolor='black',  
    borderwidth=1,  
    bgcolor='white', 
    opacity=0.9  
)
fig2.add_annotation(
    xref='x',
    yref='y',
    x=0,
    y=weekday_order.index('Thu'),
    text='<b>students on their<br>way to parties</b>',
    showarrow=True,
    arrowhead=1,
    arrowcolor='white',
    arrowside='none',
    ax=-10,
    ay=-140,
    font=dict(color='black', size=10),  
    bordercolor='black',  
    borderwidth=1,  
    bgcolor='white', 
    opacity=0.9  
)
fig2.add_annotation(
    xref='x',
    yref='y',
    x=5,
    y=weekday_order.index('Sat'),
    text='<b>people returning<br>from parties</b>',
    showarrow=True,
    arrowhead=1,
    arrowcolor='white',
    arrowside='none',
    ax=-40,
    ay=-205,
    font=dict(color='black', size=10),  
    bordercolor='black',  
    borderwidth=1,  
    bgcolor='white', 
    opacity=0.9  
)

#########################################################################################################
# PAGE LAYOUT

layout = html.Div([
    html.H2("Which time of day and night is the noisiest in Leuven?"),
    html.P("This heatmap highlights the noisiest hours of the day and night in Leuven throughout the different days of the week."),
    html.Div(
        className="plot-container",  
        style={'padding': '20px', 'max-width': '90vw', 'justify-content': 'center'},
        children=[
            html.Div(id="heatmap-container"),
            html.Button("Entire day", id="entire-day-button", n_clicks=0),
            html.Button("At night", id="at-night-button", n_clicks=0),
])])


#########################################################################################################
# CALLBACK UPDATE GRAPH

@callback(
    Output("heatmap-container", "children"),
    [Input("entire-day-button", "n_clicks"),
     Input("at-night-button", "n_clicks")]
)
def update_figure(entire_day_clicks, at_night_clicks):
    ctx = dash.callback_context

    #when it is not triggered yet (at the beginning)
    if not ctx.triggered:
        return dcc.Graph(figure=fig1)
    
    #find which button has been triggered
    clicked_button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if clicked_button_id == "entire-day-button":
        return dcc.Graph(figure=fig1)
    elif clicked_button_id == "at-night-button":
        return dcc.Graph(figure=fig2)
