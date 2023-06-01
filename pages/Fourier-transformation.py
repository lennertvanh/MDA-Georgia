#########################################################################################################
# PACKAGES

import dash
from dash import html, dcc, callback
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import numpy as np
from scipy.fft import fft, fftfreq

dash.register_page(__name__)


#########################################################################################################
# PAGE LAYOUT

# intercept always added
labels = ["2 hours","4 hours","6 hours","12 hours","day", "half-week",  "week", "month",  "3 months",  "6 months",  "year"]
labels_complete = ["intercept","2 hours","4 hours","6 hours","12 hours","day", "half-week",  "week", "month",  "3 months",  "6 months",  "year"]

x = [1, 2, 3, 4, 5]
y = [10, 5, 7, 8, 3]
fig1 = go.Figure(data=go.Scatter(x=x, y=y, mode='markers'))

# Define the HTML page layout
layout = html.Div(
    [
        html.H2("Probing the frequency spectrum for different time intervals"),
        html.P("The graph below allows us to dive into the fascinating world of noise patterns by exploring the frequency spectrum across various time intervals. By applying Fourier transformation to the recorded noise levels, we gain insight into the periodic components and dominant frequencies present in the noise data. Through the checkboxes, you can selectively examine the signal fit for different time resolutions, ranging from short intervals of 2 hours to longer durations of up to a year."),
        html.P("In the frequency domain, the peaks match exactly the frequencies that we would expect: 12 hours, day, week, month... When these frequencies are kept to reconstruct the signal in the time domain, a good approximation is obtained when one zooms in on a shorter time interval with all the checkboxes on the right selected and the 'Add complete time series' is also selected."),
        html.Div(
            className="plot-container",  # Add the CSS class to this div element
            style={'display': 'flex', 'justify-content': 'center'},
            children=[
                html.Div(
                    style={'width': '15%'},
                    children=[
                        dcc.Checklist(
                            id='checklist-add-complete-time-series',
                            options=[
                                {"label": "Add complete time series", "value": "full-series"},
                                {"label": "Frequency domain", "value": "freq-domain"}
                            ],
                            value=[],
                            style={'margin-bottom': '5px', 'display': 'block'},
                            labelStyle={'display': 'block'}
                        )
                    ]
                ),
                html.Div(
                    style={'width': '70%', 'position': 'relative'},
                    children=[
                        dcc.Graph(id='graph-Fourier', figure=fig1)
                    ]
                ),
                html.Div(
                    style={'width': '15%', 'position': 'relative'},
                    children=[
                        html.Div(
                            children=[
                                dcc.Checklist(
                                    id='checklist',
                                    options=[{'label': label, 'value': label} for label in labels],
                                    value=["year"],
                                    style={'margin-bottom': '5px', 'display': 'block'},
                                    labelStyle={'display': 'block'}
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


#########################################################################################################
# DATA

data_noise = pd.read_csv("Data for visualization/hourly_noisedata_2022.csv")
data_Namen = data_noise[data_noise["description"]=="MP 03: Naamsestraat 62 Taste"]

# Fourier transformation

# Number of sample points
N = len(data_Namen)
# Sample spacing
T = 3600  # in seconds (1 hour)
x = np.linspace(0.0, N * T, N, endpoint=False)
y = data_Namen["laeq"].to_numpy()

# Compute the FFT
yf = fft(y)
xf = fftfreq(N, T)[:N//2]

# Selected frequencies
selected_frequencies = [0,    1/2, 1/4,  1/6 , 1 / 12,   1/24,  2 / (7 * 24),  1 / (7 * 24),  1 / 720,  1 / 2160,  1 / (24 * (365 / 2)), 1/(24*365)]
selected_frequencies_not_complete = [ 1/2, 1/4,  1/6,  1 / 12,   1/24,  2 / (7 * 24),  1 / (7 * 24),  1 / 720,  1 / 2160,  1 / (24 * (365 / 2)), 1/(24*365)]
# 0 frequency for the "intercept"
selected_frequencies = [freq / 3600 for freq in selected_frequencies]  # Convert to Hz

# Find the indices corresponding to the selected frequencies
selected_indices = [np.abs(xf - freq).argmin() for freq in selected_frequencies]

# Retrieve the selected peaks from the FFT result
selected_peaks = yf[selected_indices]

laeq = data_Namen["laeq"]
laeq_standardized = data_Namen["laeq_standardized"]



#########################################################################################################
# VISUALIZATION

# Fourier plot
# Create the Plotly scatter plot
fig_FFT = go.Figure(data=go.Scatter(x=3600*xf, y=2.0/N * np.abs(yf[0:N//2]), mode='lines', line=dict(color='#2A9D8F')))

# Customize the plot layout
fig_FFT.update_layout(
    title=dict(text="Frequency Spectrum - dominant frequencies are 12 hours, day, half-week and week",
               x=0.5,
               font=dict(color="white", size=24)
               ),
    xaxis=dict(title='Frequency (1/hour)',
               showgrid=True,
               zeroline=False,
               gridcolor='rgba(255, 255, 255, 0.1)',
               title_font=dict(color="white", size=18),
               type="log"),
    yaxis=dict(title='Amplitude',
               showgrid=True,
               zeroline=True,
               gridcolor='rgba(255, 255, 255, 0.1)',
               title_font=dict(color="white", size=18),
               type="log"),
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
    paper_bgcolor='rgba(0,0,0,0)'  # Set the paper background color to transparent
)
fig_FFT.update_xaxes(color="white", gridwidth=2)
fig_FFT.update_yaxes(color="white")

# Add vertical lines
for x, label in zip(selected_frequencies_not_complete, labels):
    fig_FFT.add_shape(type="line",
                  x0=x,
                  y0=fig_FFT.data[0].y.min(),
                  x1=x,
                  y1=fig_FFT.data[0].y.max(),
                  line=dict(color="#EB862E", width=1, dash="dash")
                  )
    fig_FFT.add_annotation(
        x=np.log10(x),
        y=np.log10(fig_FFT.data[0].y.max()),  # Adjust the y position
        text=label,
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-50,  # Adjust the y offset
        font=dict(color='white'),  # Set the text color to red
        arrowcolor='white'  # Set the arrow color to red
    )


#########################################################################################################
# CALLBACK UPDATE FIGURE

@callback(
    Output('graph-Fourier', 'figure'),
    [Input('checklist', 'value'),Input('checklist-add-complete-time-series','value')],
    suppress_callback_exceptions=True #in the app?  id not found only at the beginning/starting of the subpage, afterwards, it works
)
def update_figure(selected_values,selected_value_add_series):
     
    t = np.linspace(0, len(data_Namen)-1,num=len(data_Namen))
    reconstructed_signal = np.zeros(len(t))

    for i in range(len(selected_peaks)):
        if(labels_complete[i] in selected_values):
            amplitude = selected_peaks[i]
            frequency = selected_frequencies[i]
            reconstructed_signal += np.real(amplitude * np.exp(1j * 2*np.pi* frequency * (t*3600)))

    if(len(selected_values)!=0):
        reconstructed_signal = reconstructed_signal*2/max(reconstructed_signal)

    #plot with standardized values

    # Creating the scatter plot using go.Scatter
    new_figure = go.Figure(data=go.Scatter(
        #x=data_Namen['time'],
        x = t,
        y=reconstructed_signal,
        mode='lines'
    ))

    # Customizing the plot layout
    new_figure.update_layout(
        title='Scatter Plot of LAEQ over Time',
        xaxis=dict(title='Time (hours)'),
        yaxis=dict(title='LAEQ'),
        plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
        paper_bgcolor='rgba(0,0,0,0)'  # Set the paper background color to transparent
    )

    # Creating the scatter plot for reconstructed_signal
    trace1 = go.Scatter(
        x=t,
        y=reconstructed_signal,
        mode='lines',
        name='Reconstructed Signal',
        line=dict(color='#EB862E'),
        opacity=0.5
    )

    # Creating the scatter plot for laeq_standardized
    trace2 = go.Scatter(
        y=laeq_standardized,
        mode='lines',
        name='Standardized average<br>noise level',
        opacity=0.8,
        line=dict(color='#2A9D8F')
    )

    if("full-series" in selected_value_add_series):
        # Create the combined plot
        new_figure = go.Figure(data=[trace1, trace2])
    else:
        new_figure = go.Figure(data=[trace1])

    new_figure.update_layout(
        title=dict(text='Play with the checklist on the right, select all the boxes and zoom in to see the "fit"',
            x=0.5,
            font=dict(color="white", size=24)
            ),
        xaxis=dict(title='',
            showgrid=True,
            zeroline=False,
            gridcolor='rgba(255, 255, 255, 0.1)',
            title_font=dict(color="white", size=18)),
            yaxis=dict(title='',
               showgrid=True,
               zeroline=True,
               gridcolor='rgba(255, 255, 255, 0.1)',
               title_font=dict(color="white", size=18)),
        plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background color to transparent
        legend=dict(
            font=dict(color="white")  
        )
    )
    new_figure.update_xaxes(color="white", gridwidth=2)
    new_figure.update_yaxes(color="white")

    if('freq-domain' in selected_value_add_series):
        return fig_FFT
    else:
        return new_figure 
