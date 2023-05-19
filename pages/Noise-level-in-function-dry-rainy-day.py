import dash
from dash import html, dcc, callback
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

dash.register_page(__name__)

weather_data = pd.read_csv("Data/daily_weatherdata_2022.csv", header = 0, sep=',')

cutoff_rain_day = 0.002

weather_data["bool_rainday"] = weather_data["LC_DAILYRAIN"] > cutoff_rain_day

data_noise = pd.read_csv('Data/combined_noisedata_2022.csv', header=0, sep=',', parse_dates=["result_date"])

average_noise = data_noise.groupby('result_month')['laeq'].mean()

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

#figure 1
""" 
fig = go.Figure(data=go.Bar(x=months, y=average_noise))

# Set the color of bars based on the value
#fig.update_traces(marker=dict(color=['red' if val < 0 else 'green' for val in average_noise]))

fig.update_layout(
    title="Average noise level per month (standardized data)",
    xaxis_title="Month",
    yaxis_title="Average noise level (Laeq)"
)

fig.show() """

data_noise_merged = pd.merge(data_noise, weather_data[["Month", "Day", "bool_rainday"]], left_on=["result_month", "result_day"], right_on=["Month", "Day"], how="left")

data_noise_merged = data_noise_merged.drop_duplicates()


rainy_data = data_noise_merged[data_noise_merged["bool_rainday"]]
dry_data = data_noise_merged[~data_noise_merged["bool_rainday"]]

mean_rainy = rainy_data["laeq"].mean()

mean_total_data = data_noise["laeq"].mean()

mean_dry = dry_data["laeq"].mean()

average_noise_rainy = rainy_data.groupby('result_month')['laeq'].mean()

""" #figure 2
fig2 = go.Figure(data=go.Bar(x=months, y=average_noise_rainy))

fig2.update_layout(
    title="Average noise level per month when it is raining",
    xaxis_title="Month",
    yaxis_title="Average noise level (Laeq)"
)

fig2.show() """

#figure 3
average_noise_dry = dry_data.groupby('result_month')['laeq'].mean()

""" fig3 = go.Figure(data=go.Bar(x=months, y=average_noise_dry))

# Set the color of bars based on the value
#fig.update_traces(marker=dict(color=['red' if val < 0 else 'green' for val in average_noise]))

fig3.update_layout(
    title="Average noise level per month when it is dry",
    xaxis_title="Month",
    yaxis_title="Average noise level (Laeq)"
)

fig3.show() """



""" layout = html.Div([
    html.Div([
        html.H2("Average noise level per month (standardized data)"),
        dcc.Graph(id="plot", figure=go.Figure(data=go.Bar(x=months, y=average_noise))),
    ], style={'width': '80%', 'display': 'inline-block'}),

    html.Div([
        html.Button("Total Year", id="total-noise", n_clicks=0),
        html.Button("Rainy Days", id="rainy-noise", n_clicks=0),
        html.Button("Dry Days", id="dry-noise", n_clicks=0),
    ], className="button-container"),

    html.Div([
        html.Div([
            html.H3("Average Noise for the Total Year"),
            html.Div(f"{mean_total_data:.2f}", id="total-noise"),
        ], className="tile"),

        html.Div([
            html.H3("Average Noise on Rainy Days"),
            html.Div(f"{mean_rainy:.2f}", id="rainy-noise"),
        ], className="tile"),

        html.Div([
            html.H3("Average Noise on Dry Days"),
            html.Div(f"{mean_dry:.2f}", id="dry-noise"),
        ], className="tile"),
    ], className="dashboard-tiles")
]) """

""" html.Div([
            html.H3("Average Noise for the Total Year"),
            html.Div(f"{mean_total_data:.2f}", id="total-noise"),
        ], className="tile"),

        html.Div([
            html.H3("Average Noise on Rainy Days"),
            html.Div(f"{mean_rainy:.2f}", id="rainy-noise"),
        ], className="tile"),

        html.Div([
            html.H3("Average Noise on Dry Days"),
            html.Div(f"{mean_dry:.2f}", id="dry-noise"),
        ], className="tile"), """


layout = html.Div([
    html.Div([
        html.H2("Average noise level per month",style={"font-family": 'Lato', "font-size": "54px", "font-weight": "250","padding":"0", "margin": "0 0 0 100px"}),
        html.Br(),
        html.H2("raw data",style={"font-family": 'Lato', "font-size": "54px", "font-weight": "250","padding":"0", "margin": "0 0 0 100px","margin-bottom":"-10px"}),
        
        
        dcc.Graph(id="plot", figure=go.Figure(data=go.Bar(x=months, y=average_noise)),style={"margin-top":"0"}),
    ], style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'top'}),


    
    html.Div([
        
        html.Div([
        html.Button(children=[
            'Total data',
            html.Br(),
            f"{mean_total_data:.2f} dB(A)",
        ],
          id="total-noise", n_clicks=0, style={'width': '250px','height':"130px","margin-bottom":"10px","margin-top":"20px","border-radius":"10px","font-size":"40px","color":"white","background":"darkmagenta"}),

        html.Br(),

        html.Button(children=[
            'Rainy days',
            html.Br(),
            f"{mean_rainy:.2f} dB(A)",
        ]
        , id="rainy-noise", n_clicks=0, style={'width': '250px','height':"130px","margin-bottom":"10px","border-radius":"10px","font-size":"40px","color":"white","background":"darkmagenta"}),

        html.Br(),

        html.Button(children=[
            'Dry days',
            html.Br(),
            f"{mean_dry:.2f} dB(A)",
        ], id="dry-noise", n_clicks=0, style={'width': '250px','height':"130px","border-radius":"10px","font-size":"40px","color":"white","background":"darkmagenta"}),
    ], className="button-container", style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '20px'}),
    
    ], className="dashboard-tiles", style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '20px'}),

    
])


@callback(
    Output("plot", "figure"),
    [Input("total-noise", "n_clicks"), Input("rainy-noise", "n_clicks"), Input("dry-noise", "n_clicks")]
)
def update_plot(total_clicks, rainy_clicks, dry_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        fig = go.Figure(data=go.Bar(x=months, y=average_noise))
        fig.update_layout(title=dict(text="Total",x=0.5),xaxis_title="Month", yaxis_title="Average Noise Level",
                          plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          title_font_family="Times New Roman",title_font=dict(size=40),
                          xaxis=dict(showgrid=True, zeroline=True),
                          yaxis=dict(showgrid=True, zeroline=True))
        fig.update_xaxes(color="black",gridwidth=5)
        fig.update_traces(marker_color='blue')
        return fig

    clicked_button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if clicked_button_id == "total-noise":
        fig = go.Figure(data=go.Bar(x=months, y=average_noise))
        fig.update_layout(title=dict(text="Total",x=0.5),xaxis_title="Month", yaxis_title="Average Noise Level",
                          plot_bgcolor='rgba(0,0,0,0)',
                          title_font_family="Times New Roman",title_font=dict(size=40),
                          xaxis=dict(showgrid=True, zeroline=True),
                          yaxis=dict(showgrid=True, zeroline=True))
        fig.update_xaxes(color="black",gridwidth=5)
        fig.update_traces(marker_color='blue')
        return fig
    elif clicked_button_id == "rainy-noise":
        fig = go.Figure(data=go.Bar(x=months, y=average_noise_rainy))
        fig.update_layout(title=dict(text="Rainy",x=0.5),xaxis_title="Month", yaxis_title="Average Noise Level (Rainy)",
                          plot_bgcolor='rgba(0,0,0,0)',
                          title_font_family="Times New Roman",title_font=dict(size=40),
                          xaxis=dict(showgrid=True, zeroline=True),
                          yaxis=dict(showgrid=True, zeroline=True))
        fig.update_xaxes(color="black",gridwidth=5)
        fig.update_traces(marker_color='blue')
        return fig
    elif clicked_button_id == "dry-noise":
        fig = go.Figure(data=go.Bar(x=months, y=average_noise_dry))
        fig.update_layout(title = dict(text="Dry",x=0.5),xaxis_title="Month", yaxis_title="Average Noise Level (Dry)",
                          title_font_family="Times New Roman",title_font=dict(size=40),
                          plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          xaxis=dict(showgrid=True, zeroline=True),
                          yaxis=dict(showgrid=True, zeroline=True))
        fig.update_xaxes(color="black",gridwidth=5)
        fig.update_traces(marker_color='blue')
        return fig