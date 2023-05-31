#########################################################################################################
# PACKAGES

import dash
from dash import html, dcc, callback
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

dash.register_page(__name__)


#########################################################################################################
# DATA

data_noise = pd.read_csv("Data for visualization/daily_noisedata_2022.csv")

#kuleuven calendar
#https://www.kuleuven.be/over-kuleuven/kalenders/kalenders-21-22/academische-kalender-2021-2022-ku-leuven-campus-leuven
#https://www.kuleuven.be/over-kuleuven/kalenders/kalenders-22-23/ku-leuven-leuven
holidays_unif_begin = [[1,1],[4,2],[5,28],[12,24]] #month then day
holidays_unif_end = [[2,13],[4,18],[9,26],[12,31]]

#https://www.belgieschoolvakanties.be/2021/
#https://www.vlaanderenvakantieland.be/artikel/schoolvakanties-en-feestdagen-2022
holidays_school_begin = [[1,1],[2,26],[4,2],[7,1],[10,29],[12,24]] #month then day
holidays_school_end = [[1,9],[3,6],[4,18],[8,31],[11,6],[12,31]]

#for universities
# Create a new column for holiday indicator
data_noise['is_holiday'] = False

# Iterate over each row in the DataFrame
for index, row in data_noise.iterrows():
    result_month = row['month']
    result_day = row['day']
    
    # Check if the current date is a holiday
    for begin, end in zip(holidays_unif_begin, holidays_unif_end):
        if begin[0] <= result_month <= end[0] and begin[1] <= result_day <= end[1]:
            data_noise.at[index, 'is_holiday'] = True
            break

#pre-university school
# Create a new column for holiday indicator
data_noise['is_holiday_school'] = False

# Iterate over each row in the DataFrame
for index, row in data_noise.iterrows():
    result_month = row['month']
    result_day = row['day']
    
    # Check if the current date is a holiday
    for begin, end in zip(holidays_school_begin, holidays_school_end):
        if begin[0] <= result_month <= end[0] and begin[1] <= result_day <= end[1]:
            data_noise.at[index, 'is_holiday_school'] = True
            break


# Separate the data into holiday and normal day groups
holiday_data = data_noise[data_noise['is_holiday'] == 1]
normal_day_data = data_noise[data_noise['is_holiday'] == 0]

# Define the radio item options
radio_options = [
    {'label': 'KU Leuven Holidays', 'value': 'university'},
    {'label': 'Undergraduate school Holidays', 'value': 'undergraduate'}
]

#########################################################################################################
# PAGE LAYOUT

# Define the HTML layout
layout = html.Div(
    children=[
        html.H2("Is Leuven more or less noisy during holidays?"),
        html.P("This violinplot compares the daily average noise levels in Leuven during holidays vs. regular days. Moreover, a distinction is made between primary/secondary school holidays and university holidays. We notice that it seems to be less noisy during school holidays, the effect is a bit more outspoken for KUL holidays."),
        html.Div(
            className="plot-container",  
            style={'display': 'flex', 'justify-content': 'center'},
            children=[
                html.Div(
                    style={'width': '5%'},
                    children=[
                        html.Div('')
                    ]
                ),
                html.Div(
                    style={'padding': '10px', 'max-width': '90vw', 'justify-content': 'center'},
                    children=[
                        dcc.Graph(id='graph')
                    ]
                ),
                html.Div(
                    style={'width': '20%', 'position': 'relative'},
                    children=[
                        html.Div(
                            dcc.RadioItems(
                                id='radio-item',
                                options=radio_options,
                                value='university',
                                style={'margin-top': '200px'},
                                labelStyle={'display': 'block', 'margin-bottom': '5px'}
                            )
                        )
                    ]
                )
            ]
        )
    ]
)


#########################################################################################################
# VISUALIZATION

# Create a trace for the holiday distribution
trace1 = go.Violin(
    x=holiday_data['is_holiday'],
    y=holiday_data['laeq'],
    name='Holiday',
    side='negative',
    box_visible=True,
    meanline_visible=True,
    hovertemplate='Holiday<br>Noise Level: %{y.2f} dB(A)',
    hoverlabel=dict(namelength=0),
    fillcolor='rgba(255, 132, 232, 0.6)',  
    line=dict(color='rgba(0, 0, 0, 0.8)', width=1)  
)

# Create a trace for the normal day distribution
trace2 = go.Violin(
    x=holiday_data['is_holiday'], #to put the two graphs next to each other instead of separately
    y=normal_day_data['laeq'],
    name='Normal Day',
    side='positive',
    box_visible=True,
    meanline_visible=True,
    hovertemplate='Normal Day<br>Noise Level: %{y.2f} dB(A)',
    hoverlabel=dict(namelength=0),
    fillcolor='rgba(230, 175, 46, 0.6)',
    line=dict(color='rgba(0, 0, 0, 0.8)', width=1)  
)

# Create the layout for the plot
layout_fig1 = go.Layout(
    title=dict(
        text='Noise levels during holidays and normal days <br>(KU Leuven holidays)',
        x=0.5,
        xanchor='center',
        font=dict(color="white", size=24)
    ),
    title_font=dict(size=24, color="white"),  
    xaxis=dict(
        {'title': 'Holiday vs normal day'}, 
        range = [-0.5, 0.5], 
        tickvals = [1,0], 
        ticktext = ["false",'Holiday - Normal day'],
        title_font=dict(color="white", size = 18),
        tickfont=dict(color='rgba(0, 0, 0, 0)'),
        gridcolor='rgba(255, 255, 255, 0.2)'),
    yaxis=dict(
        {'title': 'Noise Level (in dB(A))'},
        title_font=dict(color="white", size = 18),
        tickfont=dict(color="white"),
        gridcolor='rgba(255, 255, 255, 0.2)'),
    violingap=0,  # Set the gap between violins to 0 for overlapping
    plot_bgcolor='rgba(0,0,0,0)',  
    paper_bgcolor='rgba(0,0,0,0)',  
    legend = dict(font=dict(color='white'))
)

# Create the figure and add the traces
fig1 = go.Figure(data=[trace1, trace2], layout=layout_fig1)

# Set autosize to False and specify a larger width for the plot
fig1.update_layout(autosize=False, width=800)

#for pre-university school

# Separate the data into holiday and normal day groups
holiday_data = data_noise[data_noise['is_holiday_school'] == 1]
normal_day_data = data_noise[data_noise['is_holiday_school'] == 0]

# Create a trace for the holiday distribution
trace1 = go.Violin(
    x=holiday_data['is_holiday_school'],
    y=holiday_data['laeq'],
    name='Holiday',
    side='negative',
    box_visible=True,
    meanline_visible=True,
    hovertemplate='Holiday<br>Noise Level: %{y.2f} dB(A)',
    hoverlabel=dict(namelength=0),
    fillcolor='rgba(255, 132, 232, 0.6)', 
    line=dict(color='rgba(0, 0, 0, 0.8)', width=1)  
)

# Create a trace for the normal day distribution
trace2 = go.Violin(
    x=holiday_data['is_holiday_school'], #to put the two graphs next to each other instead of separately
    y=normal_day_data['laeq'],
    name='Normal Day',
    side='positive',
    box_visible=True,
    meanline_visible=True,
    hovertemplate='Normal Day<br>Noise Level: %{y.2f} dB(A)',
    hoverlabel=dict(namelength=0),
    fillcolor='rgba(230, 175, 46, 0.6)',
    line=dict(color='rgba(0, 0, 0, 0.8)', width=1)  
)

# Create the layout for the plot
layout_fig2 = go.Layout(
    title=dict(
        text='Noise levels during holidays and normal days <br>(primary and secondary school holidays)',
        x=0.5,
        xanchor='center',
        font=dict(color="white", size=24)
    ),
    title_font=dict(size=24, color="white"),  
    xaxis=dict(
        {'title': 'Holiday vs normal day'}, 
        range = [-0.5, 0.5], 
        tickvals = [1,0], 
        ticktext = ["false",'Holiday - Normal day'],
        title_font=dict(color="white", size = 18),
        tickfont=dict(color='rgba(0, 0, 0, 0)'),
        gridcolor='rgba(255, 255, 255, 0.2)'),
    yaxis=dict(
        {'title': 'Noise Level (in dB(A))'},
        title_font=dict(color="white", size = 18),
        tickfont=dict(color="white"),
        gridcolor='rgba(255, 255, 255, 0.2)'),
    violingap=0,  # Set the gap between violins to 0 for overlapping
    plot_bgcolor='rgba(0,0,0,0)',  
    paper_bgcolor='rgba(0,0,0,0)',  
    legend = dict(font=dict(color='white'))
)

# Create the figure and add the traces
fig2 = go.Figure(data=[trace1, trace2], layout=layout_fig2)

# Set autosize to False and specify a larger width for the plot
fig2.update_layout(autosize=False, width=800)

#########################################################################################################
# CALLBACK UPDATE GRAPH

@callback(
    Output('graph', 'figure'),
    [Input('radio-item', 'value')]
)
def update_figure(selected_option):
    if selected_option == 'university':
        return fig1
    elif selected_option == 'undergraduate':
        return fig2
    else:
        # Handle other cases or return a default figure
        return {}