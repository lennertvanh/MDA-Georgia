#########################################################################################################
# PACKAGES

import dash
from dash import html, dcc, callback
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import numpy as np

dash.register_page(__name__)

#########################################################################################################
# DATA

trafficimportances = pd.read_csv("Data for modelling/trafficimportances.csv", index_col=0)

heavydependence = pd.read_csv("Data for modelling/heavydependence.csv", index_col=0)
heavyvalues = pd.read_csv("Data for modelling/heavyvalues.csv", index_col=0)

cardependence = pd.read_csv("Data for modelling/cardependence.csv", index_col=0)
carvalues = pd.read_csv("Data for modelling/carvalues.csv", index_col=0)

bikedependence = pd.read_csv("Data for modelling/bikedependence.csv", index_col=0)
bikevalues = pd.read_csv("Data for modelling/bikevalues.csv", index_col=0)

peddependence = pd.read_csv("Data for modelling/peddependence.csv", index_col=0)
pedvalues = pd.read_csv("Data for modelling/pedvalues.csv", index_col=0)

cormatrix = pd.read_csv("Data for modelling/cormatrix.csv", index_col=0)

heavydep = np.ravel(heavydependence)
heavyval = np.ravel(heavyvalues)

cardep = np.ravel(cardependence)
carval = np.ravel(carvalues)

bikedep = np.ravel(bikedependence)
bikeval = np.ravel(bikevalues)

peddep = np.ravel(peddependence)
pedval = np.ravel(pedvalues)


#########################################################################################################
# VISUALIZATION

feature_names = ['heavy', 'car', 'bike', 'pedestrian']
importances = np.ravel(trafficimportances)

fig1 = go.Figure()

fig1.add_trace(go.Bar(
    x=importances,
    y=feature_names,
    orientation='h',
    marker=dict(color="#E6AF2E"),
    hovertemplate='<b>Feature:</b> %{y}<br>' +
                      '<b>Mean MSE increase:</b> %{x:.2f}<extra></extra>'
))

fig1.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    title=dict(text='Traffic random forest permutation feature importance', font=dict(color="white", size=20)),
    xaxis_title='Mean MSE increase',
    yaxis_title='Feature name',
    yaxis=dict(showgrid=True, zeroline=True, gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =16),tickfont=dict(color="white"),),
    xaxis=dict(showgrid=True, zeroline=True,  gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =16),tickfont=dict(color="white"),),
    bargap=0.1,  # Set the gap between bars to 0.1 (adjust as needed)
    margin=dict(l=0, r=20, t=40, b=0)  # Set all margins to 0
)

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=heavyval,
    y=heavydep,
    marker=dict(
    color="#E6AF2E"
    ),
    hovertemplate='<b>Conditional average noise:</b>: %{y:.2f} dB(A)<br>',
    hoverlabel=dict(namelength=0)
))

fig2.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    title=dict(text='Partial dependence', font=dict(color="white", size=24)),
    xaxis_title='Number of heavy vehicles',
    yaxis_title='Conditional average noise',
    yaxis=dict(showgrid=True, zeroline=False, gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),tickfont=dict(color="white"),),
    xaxis=dict(showgrid=True, zeroline=False,  gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),tickfont=dict(color="white"),),
    width=100,  # Set the width of the plot to 100 pixels
    margin=dict(l=0, r=20, t=40, b=0)  # Set all margins to 0
)

colorscale = [[0, '#2A9D8F'], [1, '#EB862E']]

fig3 = go.Figure(data=go.Heatmap(
    z=cormatrix,
    x=['Heavy', 'Car', 'Bike ', 'Pedestrian'],
    y=['Heavy', 'Car', 'Bike', 'Pedestrian'],
    colorscale='Reds',
    hovertemplate='Correlation between %{x} and %{y}: %{z:.2f}',
    hoverlabel=dict(namelength=0),
    colorbar=dict(
        tickfont=dict(color='white')  
    )
))

fig3.update_layout(
    title={
        'text': 'Correlation matrix of the traffic features',
        'x': 0.5,  
        'xanchor': 'center',  
        'font': {'color': 'white', 'size' : 24}  
    },
    xaxis=dict(
        title_font=dict(color="white", size=18),
        tickfont=dict(color="white"),
        gridcolor='rgba(0, 0, 0, 0)', 
        zeroline=False  
    ),
    yaxis=dict(
        title_font=dict(color="white", size=18),
        tickfont=dict(color="white"),
        gridcolor='rgba(0, 0, 0, 0)',  
    ),
    plot_bgcolor='rgba(0,0,0,0)', 
    paper_bgcolor='rgba(0,0,0,0)',
)


#########################################################################################################
# PAGE LAYOUT

# Define the HTML page layout
layout = html.Div(
    children=[
        html.Div(
            [
                html.H2("Traffic model"),
                html.P("We scraped traffic data from Telraam, consisting of two weeks of complete observations between June 1 and June 14, measured between 3AM and 7PM. This is enough data for us to investigate how traffic variables impact the noise. A separate random forest was trained for this purpose, including the amount of heavy (heavier than a passenger vehicle), car, bicycle, and pedestrian traffic."),

            ]
        ),
html.Div(
                    children=[
                        dcc.Graph(
                            id='trafimp-plot-id',
                            figure=fig1,
                            style={'height': '100%', 'width': '600px'},
                        ),
                    ],
            style={'display': 'flex', 'flex': '45%', 'justify-content': 'center', 'align-items': 'center'}
                ),
html.Div(
            children = [
        html.P("The model picks out bicycles as being by far the best predictor of noise, followed by cars. This may seem surprising at first because cars are the most frequent source of noise. They are, however, also the quietest noise source on average. Singing and shouting tends to be much louder which is associated with bicycles and pedestrians. So from our noise analysis we would expect bikes and pedestrians to be the biggest source of noise, however it should be noted that bike and pedestrian have a relatively high correlation. Since like most statistical models, a random forest is not a causal model. It can not directly identify the cause of noise, it can only point to variables that correlate with noise. As such, highly correlated features can lead to importance transferring from one to the other. Analysis of 2-way interaction plots of the traffic features did not provide additional insight into their dependence structure. We plot the correlation matrix for completeness."),
                ]
),
html.Div(
    children=[
        html.Br(),
        html.H3("Correlation Matrix"),
        dcc.Graph(
            id='correlation-heatmap',
            figure=fig3,
            style={'text-align': 'center', 'margin': 'auto', 'justify-content': 'center', 'align-items': 'center', 'width': '500px'}
        ),
        ],
),
html.Div(
            children = [
        html.Br(),
        html.H3("Individual effects",style={"margin-left":"100px"}),
        html.P("Also here, we provide the isolated effects of the features"),
            ]
),

html.Div(
            [
                html.Div(style={'flex': '10%'}),
                     html.Div(
            children=[
          dcc.Graph(
            id='trafdepen-plot-id',
            figure=fig2,
            style={'width': '800px', 'height': '100%', 'margin-left': '148px'},
          ),
        ],
        style={'flex': '45%', 'display': 'inline-block', 'justify-content': 'center', 'align-items': 'center'}
      ),
html.Div(
                    children=[
                        html.Label('Select feature', style={'font-size': '25px'}),
                        dcc.RadioItems(
                            id='radio-item-trafpredictor',
                            options=[
                                {'label': 'Heavy', 'value': 'option-heavy'},
                                {'label': 'Car', 'value': 'option-car'},
                                {'label': 'Bike', 'value': 'option-bike'},
                                {'label': 'Pedestrian', 'value': 'option-pedestrian'},
                            ],
                            value='option-heavy',
                            labelStyle={'display': 'block','margin-top':'10px','font-size': '20px'}
                        ),
    html.Div(id='radio-item-trafname',style={"margin-top":"40px"})
    ],
    style={'flex': '10%', 'margin': '30px', 'vertical-align': 'top', 'display': 'inline-block'}
  ),
html.Div(
            children=[
                html.P("The marginal dependence plots reflect the same structure where bikes and cars are the most important traffic determinants of noise. Interesting is that the noise mostly increases in the beginning of the features' range, after which there is a ceiling effect. Heavy and pedestrian appear to fluctuate randomly within a small range."),

            ],
            style={'margin-top': '50px'}
)
            ]
)
    ]
)


#########################################################################################################
# CALLBACK UPDATE FIGURE

@callback(
    [Output('trafdepen-plot-id', 'figure'),
     Output('radio-item-trafname', 'children')],
    [Input('radio-item-trafpredictor', 'value')],
)
def update_figure3(feat):
    text=""
    depenfeat = None
    valuefeat = None

    if(feat=="option-heavy"):
        depenfeat = heavydep
        valuefeat = heavyval
        feature = "Number of heavy vehicles"
    elif(feat=="option-car"):
        depenfeat = cardep
        valuefeat = carval
        feature = "Number of cars"
    elif(feat == "option-bike"):
        depenfeat = bikedep
        valuefeat = bikeval
        feature = "Number of bikes"
    elif(feat == "option-pedestrian"):
        depenfeat = peddep
        valuefeat = pedval
        feature = "Number of pedestrians"

    values = np.ravel(valuefeat)
    means = np.ravel(depenfeat)

    fig_updated = go.Figure()

    fig_updated.add_trace(go.Scatter(
        x=values,
        y=means,
        marker=dict(
            color="#E6AF2E"
        ),
        hovertemplate='<b>Conditional average noise:</b> %{y:.2f} dB(A)<br>',
        hoverlabel=dict(namelength=0)
    ))

    fig_updated.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        title=dict(text='Partial dependence', font=dict(color="white", size=24)),
        xaxis_title=feature,
        yaxis_title='Conditional average noise',
        yaxis=dict(showgrid=True, zeroline=False, gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),tickfont=dict(color="white"),),
        xaxis=dict(showgrid=True, zeroline=False,  gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),tickfont=dict(color="white"),),
        margin=dict(l=0, r=20, t=40, b=0)  # Set all margins to 0
    )

    return fig_updated, html.P(text, style={'white-space': 'pre-line','margin':'0'})