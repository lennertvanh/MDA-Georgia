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

truevalues = pd.read_csv("Data for modelling/traffictestset.csv", index_col=0)

predicted = pd.read_csv("Data for modelling/xgbpred.csv", index_col=0)

trueval = np.ravel(truevalues)
pred = np.ravel(predicted)

#########################################################################################################
# VISUALIZATION

fig = go.Figure()
fig.add_trace(go.Scatter(
  x=trueval,
  y=pred,
  orientation='v',
  mode='markers',
  marker=dict(
    color="#E6AF2E"
  ),
    showlegend=False,
    hovertemplate="<b>True Value:</b> %{x:.2f}<br>" +
                  "<b>Predicted Value:</b> %{y:.2f}<extra></extra>"
))

line = go.Scatter(
    x=[min(trueval), max(trueval)],
    y=[min(trueval), max(trueval)],
    mode='lines',
    name='y=x',
    line=dict(
        color='white',
        width=2,
        dash='solid'
    ),
    showlegend = False
)
fig.add_trace(line)

fig.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    title=dict(text='True values vs XGBoost predictions', font=dict(color="white", size=24)),
    xaxis_title='True Noise level (dB(A))',
    yaxis_title='Predicted Noise Level (dB(A))',
    yaxis=dict(showgrid=True, zeroline=True, gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),tickfont=dict(color="white"),),
    xaxis=dict(showgrid=True, zeroline=True,  gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),tickfont=dict(color="white"),),
    #width=400,  # Set the width of the plot to 400 pixels
    margin=dict(l=0, r=20, t=40, b=0)
)

#########################################################################################################
# PAGE LAYOUT

# Define the HTML page layout
layout = html.Div(
    children=[
        html.Div(
            [
                html.H2("XGBoost"),
                html.P("After all the previous modelling focused on gaining insight, we also wanted to purely see how much of the variation in noise can be predicted just using variables about the time, weather and traffic. For this we used XGBoost, a gradient boosting machine that's known as one of the most performant algorithms for predicting tabular data currently in existence. The XGBoost model was trained on cloud with an extensive cross-validated grid search and reached a prediction R squared of 0.892. Its predictions are plotted against the true values on a small test set from the traffic data.")
                ]
        ),
      html.Div(style={'flex': '15%'}),
      html.Div(
        children=[
          dcc.Graph(
            id='pred-plot-id',
            figure=fig,
            style={'width': '800px', 'text-align': 'center', 'margin': 'auto', 'justify-content': 'center', 'align-items': 'center'},
          ),
        ],
        style={'flex': '35%'}
      ),
        html.Div(
            children=[
                html.P("If the model's predictions were perfect, they would all be on the white line bisecting the plot. A point above the white line means the model has overpredicted, one below the white line means it has underpredicted. In this case the model has 53% overpredictions and 47% underpredictions, showing that it is well centered."),
                html.P("The previous random forest models sometimes have difficulty predicting high noise levels, the XGBoost model appears to suffer from this less. XGBoost offers less explainability than the random forests because it automatically applies regularization, gradient boosting and variable selection methods. The only reasoning it offers as to why a variable was included is because it somehow improves predictions. Nonetheless, it is remarkable that almost 90% of the variation in noise can be predicted using the time, the weather, and the amount of traffic in the surrounding area.")
            ]
        )
    ]
  )






#########################################################################################################
# CALLBACK UPDATE FIGURE

#@callback(
    
#)
#def update_figure():
#    return None
