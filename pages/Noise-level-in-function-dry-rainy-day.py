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

# Define global variable to keep track of the previous clicked value of the button
global prev_clicked_button_id
prev_clicked_button_id = ""

# Loading the weather & noise data
weather_data = pd.read_csv("Data for visualization/daily_weatherdata_2022.csv", header = 0, sep=',')
data_noise = pd.read_csv("Data for visualization/daily_noisedata_2022.csv", header=0, sep=',', parse_dates=["date"])

# Define the cutoff value of the rain, i.e. 0.2mm
cutoff_rain_day = 0.0002

# Create the column boolean variable that indicates if it is a rainy day or not
weather_data["bool_rainday"] = weather_data["LC_DAILYRAIN"] > cutoff_rain_day

# Compute average noise for every month
average_noise = data_noise.groupby('date')['laeq'].mean()

# Array with the abbreviation of the months
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# Merge the noise and weather data to know in the noise data for every day if it is a rainy or dry day
data_noise_merged = pd.merge(data_noise, weather_data[["Month", "Day", "bool_rainday"]], left_on=["month", "day"], right_on=["Month", "Day"], how="left")

# Remove duplicate rows
data_noise_merged = data_noise_merged.drop_duplicates()

# Split the merged data into the dry and rainy days
rainy_data = data_noise_merged[data_noise_merged["bool_rainday"]]
dry_data = data_noise_merged[~data_noise_merged["bool_rainday"]]

# Compute the total means for total, rainy and dry data
mean_rainy = rainy_data["laeq"].mean()
mean_total_data = data_noise["laeq"].mean()
mean_dry = dry_data["laeq"].mean()

# Average noise for rainy data per month
average_noise_rainy = rainy_data.groupby('month')['laeq'].mean()

#average noise for dry data per month
average_noise_dry = dry_data.groupby('month')['laeq'].mean()

#standardize the "total" data
mean_average_noise = average_noise.mean()
std_average_noise = average_noise.std()
average_noise_std = (average_noise-mean_average_noise)/std_average_noise

#compute per month and standardize the rainy data
average_noise_rainy = rainy_data.groupby('month')['laeq'].mean()
mean_average_noise_rainy = average_noise_rainy.mean()
std_average_noise_rainy = average_noise_rainy.std()
average_noise_rainy_std = (average_noise_rainy-mean_average_noise_rainy)/std_average_noise_rainy

#compute per month and standardize the dry data
average_noise_dry= dry_data.groupby('month')['laeq'].mean()
mean_average_noise_dry = average_noise_dry.mean()
std_average_noise_dry = average_noise_dry.std()
average_noise_dry_std = (average_noise_dry-mean_average_noise_dry)/std_average_noise_dry

#########################################################################################################
# PAGE LAYOUT

#define the html file: all the text, the place of the plot, buttons and radioItem
layout = html.Div([
    #title
    html.Div([
        html.H2("Average noise level per month"),
        html.Br(),
        dcc.RadioItems(
        id="data-type",
        options=[
            #options for the input
            {"label": "Raw Data", "value": "raw"},
            {"label": "Standardized Values", "value": "standardized"},
        ],
        value="raw", #initial value of the input
        labelStyle={"display": "inline-block"},
        style = {"margin-left":"100px","font-size":"20px"},
        inputStyle={
        "width": "20px",
        "height": "20px",
        "margin-right": "10px",
        "margin-left": "10px"
    },
    ),

        #plot taking 80% of the width
        dcc.Graph(id="plot", figure=go.Figure(data=go.Bar(x=months, y=average_noise)),style={"margin-top":"0"}),
    ], style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'top'}),


    #place for the buttons
    html.Div([
        
        
        html.Div([

        #button total
        html.Button(children=[
            'Total data',
            html.Br(),
            f"{mean_total_data:.2f} dB(A)",
        ],
          id="total-noise", n_clicks=0),

        html.Br(), #break line

        #button rainy
        html.Button(children=[
            'Rainy days',
            html.Br(),
            f"{mean_rainy:.2f} dB(A)",
        ]
        , id="rainy-noise", n_clicks=0),

        html.Br(), #break line

        #button dry
        html.Button(children=[
            'Dry days',
            html.Br(),
            f"{mean_dry:.2f} dB(A)",
        ], id="dry-noise", n_clicks=0),
    ], className="button-container", style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '20px'}),
    
    ], className="dashboard-tiles", style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '20px'}),

    
])

#########################################################################################################
# CALLBACK UPDATE GRAPH

#outputs and inputs that have to change dynamically over time
@callback(
    Output("plot", "figure"),
    [Input("data-type","value"),
     Input("total-noise", "n_clicks"),
      Input("rainy-noise", "n_clicks"), 
      Input("dry-noise", "n_clicks")]
)

#what should be done when the inputs change
def update_plot(data_type,total_clicks, rainy_clicks, dry_clicks):
    global prev_clicked_button_id #define this variable globally in the function

    ctx = dash.callback_context

    #when it is not triggered yet (at the beginning)
    if not ctx.triggered:
        fig = go.Figure(data=go.Bar(x=months, y=average_noise))
        fig.update_layout(title=dict(text="Total",x=0.5, font=dict(
        color="white")),xaxis_title="Month", yaxis_title="Average Noise Level",
                        plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
                        paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background color to transparent
                        title_font=dict(size=24),
                        yaxis=dict(
                            showgrid=True,
                            zeroline=True,
                            gridcolor='rgba(255, 255, 255, 0.1)',
                            title_font=dict(color="white", size=18)
                        ),
                        xaxis=dict(
                            showgrid=True,
                            zeroline=True,
                            gridcolor='rgba(255, 255, 255, 0.1)',
                            title_font=dict(color="white", size=18)
                        ))
        fig.update_traces(hovertemplate='%{x}: %{y:.2f} dB(A)', hoverlabel=dict(namelength=0))
        fig.update_xaxes(color="white",gridwidth=5)
        fig.update_yaxes(color="white")
        fig.update_traces(marker=dict(color='#E6AF2E'))
        return fig

    #find which button has been triggered
    clicked_button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    #special case when the RadioItem is triggered instead of the button
    #give the button value the value of the button that was previously clicked on
    if str(clicked_button_id)=="data-type":
        if prev_clicked_button_id == "":
            clicked_button_id="total-noise"
        else:
            clicked_button_id=prev_clicked_button_id
    else:
        prev_clicked_button_id=clicked_button_id

    #chose which plot to show now that an input has been triggered
    if data_type == "raw":
        if clicked_button_id == "total-noise":
            #initialize the plot with the data
            fig = go.Figure(data=go.Bar(x=months, y=average_noise))
            fig.update_layout(title=dict(text="Total",x=0.5, font=dict(
            color="white")),xaxis_title="Month", yaxis_title="Average Noise Level",
                            plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
                            paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background color to transparent
                            title_font=dict(size=24),
                            yaxis=dict(
                                showgrid=True,
                                zeroline=True,
                                gridcolor='rgba(255, 255, 255, 0.1)',
                                title_font=dict(color="white", size=18)
                            ),
                            xaxis=dict(
                                showgrid=True,
                                zeroline=True,
                                gridcolor='rgba(255, 255, 255, 0.1)',
                                title_font=dict(color="white", size=18)
                            ))
            fig.update_traces(hovertemplate='%{x}: %{y:.2f} dB(A)', hoverlabel=dict(namelength=0))
            fig.update_xaxes(color="white",gridwidth=5)
            fig.update_yaxes(color="white")
            fig.update_traces(marker=dict(color='#E6AF2E'))
            return fig
        elif clicked_button_id == "rainy-noise":
            #initialize the plot with the data
            fig = go.Figure(data=go.Bar(x=months, y=average_noise_rainy))
            fig.update_layout(title=dict(text="Rainy",x=0.5, font=dict(
            color="white")),xaxis_title="Month", yaxis_title="Average Noise Level (Rainy)",
                            plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
                            paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background color to transparent
                            title_font=dict(size=24),
                            yaxis=dict(
                                showgrid=True,
                                zeroline=True,
                                gridcolor='rgba(255, 255, 255, 0.1)',
                                title_font=dict(color="white", size=18)
                            ),
                            xaxis=dict(
                                showgrid=True,
                                zeroline=True,
                                gridcolor='rgba(255, 255, 255, 0.1)',
                                title_font=dict(color="white", size=18)
                            ))
            fig.update_traces(hovertemplate='%{x}: %{y:.2f} dB(A)', hoverlabel=dict(namelength=0))
            fig.update_xaxes(color="white",gridwidth=5)
            fig.update_yaxes(color="white")
            fig.update_traces(marker_color='#E6AF2E')
            return fig
        elif clicked_button_id == "dry-noise":
            #initialize the plot with the data
            fig = go.Figure(data=go.Bar(x=months, y=average_noise_dry))
            fig.update_layout(title = dict(text="Dry",x=0.5, font=dict(
            color="white")),xaxis_title="Month", yaxis_title="Average Noise Level (Dry)",
                            title_font=dict(size=24),
                            plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
                            paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background color to transparent
                            yaxis=dict(
                                showgrid=True,
                                zeroline=True,
                                gridcolor='rgba(255, 255, 255, 0.1)',
                                title_font=dict(color="white", size=18)
                            ),
                            xaxis=dict(
                                showgrid=True,
                                zeroline=True,
                                gridcolor='rgba(255, 255, 255, 0.1)',
                                title_font=dict(color="white", size=18)
                            ))
            fig.update_traces(hovertemplate='%{x}: %{y:.2f} dB(A)', hoverlabel=dict(namelength=0))
            fig.update_xaxes(color="white",gridwidth=5)
            fig.update_yaxes(color="white")
            fig.update_traces(marker_color='#E6AF2E')
            return fig
    elif data_type=="standardized":
        if clicked_button_id == "total-noise":
            #initialize the plot with the data
            fig = go.Figure(data=go.Bar(x=months, y=average_noise_std))
            fig.update_traces(marker=dict(color=['#2A9D8F' if val < 0 else '#EB862E' for val in average_noise_std]))
            fig.update_layout(title=dict(text="Total",x=0.5, font=dict(
            color="white")),xaxis_title="Month", yaxis_title="Average Noise Level",
                            plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
                            paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background color to transparent,
                            title_font=dict(size=24),
                            yaxis=dict(
                                showgrid=True,
                                zeroline=True,
                                gridcolor='rgba(255, 255, 255, 0.1)',
                                title_font=dict(color="white", size=18)
                            ),
                            xaxis=dict(
                                showgrid=True,
                                zeroline=True,
                                gridcolor='rgba(255, 255, 255, 0.1)',
                                title_font=dict(color="white", size=18)
                            ))
            fig.update_traces(hovertemplate='%{x}: %{y:.2f}', hoverlabel=dict(namelength=0))
            fig.update_xaxes(color="white",gridwidth=5)
            fig.update_yaxes(color="white")
            return fig
        elif clicked_button_id == "rainy-noise":
            #initialize the plot with the data
            fig = go.Figure(data=go.Bar(x=months, y=average_noise_rainy_std))
            fig.update_traces(marker=dict(color=['#2A9D8F' if val < 0 else '#EB862E' for val in average_noise_rainy_std]))
            fig.update_layout(title=dict(text="Rainy",x=0.5, font=dict(
            color="white")),xaxis_title="Month", yaxis_title="Average Noise Level",
                            plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
                            paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background color to transparent
                            title_font=dict(size=24),
                            yaxis=dict(
                                showgrid=True,
                                zeroline=True,
                                gridcolor='rgba(255, 255, 255, 0.1)',
                                title_font=dict(color="white", size=18)
                            ),
                            xaxis=dict(
                                showgrid=True,
                                zeroline=True,
                                gridcolor='rgba(255, 255, 255, 0.1)',
                                title_font=dict(color="white", size=18)
                            ))
            fig.update_traces(hovertemplate='%{x}: %{y:.2f}', hoverlabel=dict(namelength=0))
            fig.update_xaxes(color="white",gridwidth=5)
            fig.update_yaxes(color="white")
            return fig
        elif clicked_button_id == "dry-noise":
            #initialize the plot with the data
            fig = go.Figure(data=go.Bar(x=months, y=average_noise_dry_std))
            fig.update_traces(marker=dict(color=['#2A9D8F' if val < 0 else '#EB862E' for val in average_noise_dry_std]))
            fig.update_layout(title=dict(text="Dry",x=0.5, font=dict(
            color="white")),xaxis_title="Month", yaxis_title="Average Noise Level",
                            plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
                            paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background color to transparent
                            title_font=dict(size=24),
                            yaxis=dict(
                                showgrid=True,
                                zeroline=True,
                                gridcolor='rgba(255, 255, 255, 0.1)',
                                title_font=dict(color="white", size=18)
                            ),
                            xaxis=dict(
                                showgrid=True,
                                zeroline=True,
                                gridcolor='rgba(255, 255, 255, 0.1)',
                                title_font=dict(color="white", size=18)
                            ))
            fig.update_traces(hovertemplate='%{x}: %{y:.2f}', hoverlabel=dict(namelength=0))
            fig.update_xaxes(color="white",gridwidth=5)
            fig.update_yaxes(color="white")
            return fig