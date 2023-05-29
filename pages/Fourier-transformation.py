import dash
from dash import html, dcc, callback
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import numpy as np
from scipy.fft import fft, fftfreq
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


dash.register_page(__name__)

#intercept always added
labels = ["2 hours","4 hours","6 hours","12 hours","day", "half-week",  "week", "month",  "3 months",  "6 months",  "year"]
labels_complete = ["intercept","2 hours","4 hours","6 hours","12 hours","day", "half-week",  "week", "month",  "3 months",  "6 months",  "year"]

x = [1, 2, 3, 4, 5]
y = [10, 5, 7, 8, 3]
fig1 = go.Figure(data=go.Scatter(x=x, y=y, mode='markers'))
fig1.update_layout(
    plot_bgcolor='rgb(0, 0, 139)'  
)

# Define the HTML layout
layout = html.Div(
    [
        html.H2("Probing the frequency spectrum for different time intervals"),
        html.P("The graph below allows us to dive into the fascinating world of noise patterns by exploring the frequency spectrum across various time intervals. By applying Fourier transformation to the recorded noise levels, we gain insight into the periodic components and dominant frequencies present in the noise data. Through the checkboxes, you can selectively examine the signal fit for different time resolutions, ranging from short intervals of 2 hours to longer durations of up to a year."),
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
                                {"label": "add complete time series", "value": "full-series"},
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



###################################################################################
#data
data_noise = pd.read_csv("Data/hourly_noisedata_2022.csv")
data_Namen = data_noise[data_noise["description"]=="MP 03: Naamsestraat 62 Taste"]

#fourier transformation
# Number of sample points
N = len(data_Namen)
# Sample spacing
T = 3600  # in seconds (1 hour)
x = np.linspace(0.0, N * T, N, endpoint=False)
y = data_Namen["laeq"].to_numpy()

# Compute the FFT
yf = fft(y)
xf = fftfreq(N, T)[:N//2]

#selected frequencies
# Selected frequencies
selected_frequencies = [0,    1/2, 1/4,  1/6 , 1 / 12,   1/24,  2 / (7 * 24),  1 / (7 * 24),  1 / 720,  1 / 2160,  1 / (24 * (365 / 2)), 1/(24*365)]
selected_frequencies_not_complete = [ 1/2, 1/4,  1/6,  1 / 12,   1/24,  2 / (7 * 24),  1 / (7 * 24),  1 / 720,  1 / 2160,  1 / (24 * (365 / 2)), 1/(24*365)]
#0 frequency for the "intercept"
selected_frequencies = [freq / 3600 for freq in selected_frequencies]  # Convert to Hz

# Find the indices corresponding to the selected frequencies
selected_indices = [np.abs(xf - freq).argmin() for freq in selected_frequencies]

# Retrieve the selected peaks from the FFT result
selected_peaks = yf[selected_indices]

laeq = data_Namen["laeq"]

pipeline = Pipeline([
    ('scaler', StandardScaler())
])

laeq_standardized = pipeline.fit_transform(laeq.values.reshape(-1, 1))
laeq_standardized = laeq_standardized.flatten()

#fourier plot
# Create the Plotly scatter plot
fig_FFT = go.Figure(data=go.Scatter(x=3600*xf, y=2.0/N * np.abs(yf[0:N//2]), mode='lines'))

# Customize the plot layout
fig_FFT.update_layout(
    title="Frequency Spectrum - dominant frequencies are 12 hours, day, half-week and week",
    xaxis_title="Frequency (1/hour)",
    yaxis_title="Amplitude",
    xaxis_type="log",
    yaxis_type="log",
    showlegend=False,
    plot_bgcolor='rgb(0,0,139)'
)

# Add vertical lines

for x, label in zip(selected_frequencies_not_complete, labels):
    fig_FFT.add_shape(type="line",
                  x0=x,
                  y0=fig_FFT.data[0].y.min(),
                  x1=x,
                  y1=fig_FFT.data[0].y.max(),
                  line=dict(color="red", width=1, dash="dash")
                  )
    fig_FFT.add_annotation(
        x=np.log10(x),
        y=np.log10(fig_FFT.data[0].y.max()),  # Adjust the y position
        text=label,
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-50  # Adjust the y offset
    )


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
        plot_bgcolor='rgb(0, 0, 139)'  
    )

    # Creating the scatter plot for reconstructed_signal
    trace1 = go.Scatter(
        x=t,
        y=reconstructed_signal,
        mode='lines',
        name='Reconstructed Signal',
        line=dict(color='red')
    )

    # Creating the scatter plot for laeq_standardized
    trace2 = go.Scatter(
        y=laeq_standardized,
        mode='lines',
        name='LAEQ Standardized',
        opacity=0.5,
        line=dict(color='blue')
    )
    if("full-series" in selected_value_add_series):
        # Create the combined plot
        new_figure = go.Figure(data=[trace1, trace2])
    else:
        new_figure = go.Figure(data=[trace1])

    new_figure.update_layout(
        title='Play with the checklist on the right, select all the boxes and zoom in to see the "fit"'
    )

    if('freq-domain' in selected_value_add_series):
        return fig_FFT
    else:
        return new_figure 
