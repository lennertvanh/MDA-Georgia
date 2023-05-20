import dash
from dash import html, dcc, callback
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

dash.register_page(__name__)

# Define the radio item options
radio_options = [
    {'label': 'University Holidays', 'value': 'university'},
    {'label': 'Pre-university Holidays', 'value': 'undergraduate'}
]

# Define the HTML layout
layout = html.Div(
    style={'display': 'flex', 'height': '50vh'},
    children=[
        html.Div(
            style={'width': '15%'},
            children=[
                html.Div('Left Content')
            ]
        ),
        html.Div(
            style={'width': '70%', 'position': 'relative'},
            children=[
                dcc.Graph(id='graph')
            ]
        ),
        html.Div(
            style={'width': '15%', 'position': 'relative'},
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








data_noise = pd.read_csv("Data/combined_noisedata_2022.csv")

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
    result_month = row['result_month']
    result_day = row['result_day']
    
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
    result_month = row['result_month']
    result_day = row['result_day']
    
    # Check if the current date is a holiday
    for begin, end in zip(holidays_school_begin, holidays_school_end):
        if begin[0] <= result_month <= end[0] and begin[1] <= result_day <= end[1]:
            data_noise.at[index, 'is_holiday_school'] = True
            break


# Separate the data into holiday and normal day groups
holiday_data = data_noise[data_noise['is_holiday'] == 1]
normal_day_data = data_noise[data_noise['is_holiday'] == 0]

# Create a trace for the holiday distribution
trace1 = go.Violin(
    x=holiday_data['is_holiday'],
    y=holiday_data['laeq'],
    name='Holiday',
    side='negative',
    box_visible=True,
    meanline_visible=True,
    hovertemplate='<b>Holiday</b><br>Noise Level: %{y} dB',
)

# Create a trace for the normal day distribution
trace2 = go.Violin(
    x=holiday_data['is_holiday'],#to put the two graphs next to each other instead of separately
    y=normal_day_data['laeq'],
    name='Normal Day',
    side='positive',
    box_visible=True,
    meanline_visible=True,
    hovertemplate='<b>Normal Day</b><br>Noise Level: %{y} dB',
)

# Create the layout for the plot
layout_fig1 = go.Layout(
    title='Comparison of Noise Levels during Holidays and Normal Days (universities)',
    xaxis={'title': 'Holiday vs normal day', 'range': [-0.5, 0.5], 'tickvals': [1,0], 'ticktext': ["false",'Holiday - Normal day']},
    yaxis={'title': 'Noise Level (dB)'},
    violingap=0,  # Set the gap between violins to 0 for overlapping
)

# Create the figure and add the traces
fig1 = go.Figure(data=[trace1, trace2], layout=layout_fig1)

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
    hovertemplate='<b>Holiday</b><br>Noise Level: %{y} dB',
)

# Create a trace for the normal day distribution
trace2 = go.Violin(
    x=holiday_data['is_holiday_school'],#to put the two graphs next to each other instead of separately
    y=normal_day_data['laeq'],
    name='Normal Day',
    side='positive',
    box_visible=True,
    meanline_visible=True,
    hovertemplate='<b>Normal Day</b><br>Noise Level: %{y} dB',
)

# Create the layout for the plot
layout_fig2 = go.Layout(
    title='Comparison of Noise Levels during Holidays and Normal Days (primary and secundary school)',
    xaxis={'title': 'Holiday vs normal day', 'range': [-0.5, 0.5], 'tickvals': [1,0], 'ticktext': ["false",'Holiday - Normal day']},
    yaxis={'title': 'Noise Level (dB)'},
    violingap=0,  # Set the gap between violins to 0 for overlapping
)

# Create the figure and add the traces
fig2 = go.Figure(data=[trace1, trace2], layout=layout_fig2)


#############################################################################################""


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
