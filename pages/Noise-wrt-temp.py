#########################################################################################################
# PACKAGES

import dash
from dash import dcc, html, callback
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output

dash.register_page(__name__)


#########################################################################################################
# DATA

# Loading noise and weather data
data_noise = pd.read_csv('Data for visualization/daily_noisedata_2022.csv', header=0, sep=',')
data_weather = pd.read_csv('Data for visualization/daily_weatherdata_2022.csv', header=0, sep=',')

# Calculate mean noise level per day
noise_per_day = data_noise.groupby(['day', 'month'])['laeq'].mean().reset_index()

# Calculate mean temperature per day
temp_per_day = data_weather.groupby(['Day', 'Month'])['LC_TEMP_QCL3'].mean().reset_index()

# Merge into 1 dataframe
merged_df = noise_per_day.merge(temp_per_day, left_on=['day', 'month'], right_on=['Day', 'Month'])
merged_df = merged_df.drop(['Day', 'Month'], axis=1)

# Divide temperature values into bins
merged_df['temp_bins'] = pd.cut(merged_df['LC_TEMP_QCL3'], bins=73) #take 5 observations per bin, i.e. 73 bins

# Calculate the mean temperature for each bin
temp_mean_per_bin = merged_df.groupby('temp_bins')['LC_TEMP_QCL3'].mean()

# Create a dictionary mapping bin labels to the mean temperature
temp_mean_dict = temp_mean_per_bin.to_dict()

# Update the temperature values with the mean temperature per bin
merged_df['LC_TEMP_QCL3'] = merged_df['temp_bins'].map(temp_mean_dict)

# Sort the dataframe based on the bins
merged_df = merged_df.sort_values('temp_bins')

# Remove the temp_bins column
merged_df = merged_df.drop('temp_bins', axis=1)



#########################################################################################################
# VISUALIZATION

# Area chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=merged_df['LC_TEMP_QCL3'],
    y=merged_df['laeq'],
    mode='lines',
    fill='tozeroy',
    line=dict(color='#E6AF2E'),
    fillcolor='rgba(230, 175, 46, 0.8)',
    name='Noise',
    hovertemplate='Temperature: %{x:.1f}°C<br>Noise Level: %{y:.2f} dB(A)',
    hoverlabel=dict(namelength=0),
))

fig.update_layout(
    title=dict(
        text="Is Leuven more quiet when it's very hot or cold outside?",
        x=0.5,
        font=dict(color="white", size=24)
    ),
    xaxis=dict(
        title='Temperature (°C)',
        showgrid=True,
        zeroline=False,
        gridcolor='rgba(255, 255, 255, 0.1)',
        title_font=dict(color="white", size=18),
        tickfont=dict(color='white')
    ),
    yaxis=dict(
        title='Average noise level (dB(A))',
        showgrid=True,
        zeroline=True,
        gridcolor='rgba(255, 255, 255, 0.1)',
        title_font=dict(color="white", size=18),
        range=[45, merged_df['laeq'].max()],
        tickfont=dict(color='white')
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    hovermode='x',
    legend=dict(
        font=dict(color='white')
    )
)



#########################################################################################################
# PAGE LAYOUT
areachart = dcc.Graph(figure=fig)

layout = html.Div([
    html.H2("Does temperature have an influence on noise?"),
    html.P("This area chart displays how the average noise level in Leuven varies with temperature. The plot indicates that extreme temperatures might correspond to lower noise levels."),
    html.Div(
        className="plot-container",
        style={'padding': '20px', 'max-width': '90vw', 'justify-content': 'center'},
        id="areachart-container",
        children=areachart  # Render the graph component inside the div
    )
])



#########################################################################################################
# NO CALLBACK NEEDED BECAUSE NO INPUT