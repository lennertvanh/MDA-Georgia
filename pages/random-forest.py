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

dayimportances = pd.read_csv("Data for modelling/RFdayimportances.csv", index_col=0)

nightimportances = pd.read_csv("Data for modelling/RFnightimportances.csv", index_col=0)

tempdependence = pd.read_csv("Data for modelling/tempdependence.csv", index_col=0)
tempvalues = pd.read_csv("Data for modelling/tempvalues.csv", index_col=0)

raindependence = pd.read_csv("Data for modelling/raindependence.csv", index_col=0)
rainvalues = pd.read_csv("Data for modelling/rainvalues.csv", index_col=0)

winddependence = pd.read_csv("Data for modelling/winddependence.csv", index_col=0)
windvalues = pd.read_csv("Data for modelling/windvalues.csv", index_col=0)

categoricaldependence = pd.read_csv("Data for modelling/Categoricalimportances.csv", index_col=0)

MSEday = 1.854
r2day = 0.874

MSEnight = 2.729
r2night = 0.689

tempdep = np.ravel(tempdependence)
tempval = np.ravel(tempvalues)

raindep = np.ravel(raindependence)
rainval = np.ravel(rainvalues)

winddep = np.ravel(winddependence)
windval = np.ravel(windvalues)


#########################################################################################################
# VISUALIZATION

feature_names = dayimportances.index.tolist()
importances = np.ravel(dayimportances)

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
    title=dict(text='Random forest permutation feature importance', font=dict(color="white", size=24)),
    xaxis_title='Mean MSE increase',
    yaxis_title='Feature name',
    yaxis=dict(showgrid=True, zeroline=True, gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),tickfont=dict(color="white"),),
    xaxis=dict(showgrid=True, zeroline=True,  gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),tickfont=dict(color="white"),),
    #width=400,  # Set the width of the plot to 400 pixels
    bargap=0.1,  # Set the gap between bars to 0.1 (adjust as needed)
    margin=dict(l=0, r=20, t=40, b=0)  
)


fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=tempval,
    y=tempdep,
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
    xaxis_title='Temperature (°C)',
    yaxis_title='Conditional average noise',
    yaxis=dict(showgrid=True, zeroline=False, gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),tickfont=dict(color="white"),),
    xaxis=dict(showgrid=True, zeroline=False,  gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),tickfont=dict(color="white"),),
    width=100,  # Set the width of the plot to 100 pixels
    margin=dict(l=0, r=20, t=40, b=0)  
)

catfeats = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'public holiday', 'KUL holiday']
catimps = np.ravel(categoricaldependence)

fig3 = go.Figure()

fig3.add_trace(go.Bar(
    x=catimps,
    y=catfeats,
    orientation='h',
    marker=dict(
        color=np.where(catimps < 0, '#EB862E', '#2A9D8F')
    ),
    hovertemplate='<b>Feature:</b>: %{y}<br>' +
                      '<b>Change in predicted sound level:</b>: %{x:.2f} dB(A)<extra></extra>',
    hoverlabel=dict(namelength=0)
))

fig3.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    title=dict(text='Partial impact of categorical predictors', font=dict(color="white", size=24)),
    xaxis_title='Change in predicted sound level (dB(A))',
    yaxis_title='Feature name',
    yaxis=dict(showgrid=True, zeroline=True, gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),tickfont=dict(color="white"),),
    xaxis=dict(showgrid=True, zeroline=True,  gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),tickfont=dict(color="white"),),
    bargap=0.1,  # Set the gap between bars to 0.1 (adjust as needed)
    margin=dict(l=0, r=20, t=40, b=0)  # Set all margins to 0
)


#########################################################################################################
# PAGE LAYOUT

# Define the HTML page layout
layout = html.Div(
    children=[
        html.Div(
            [
                html.H2("Random forest"),
                html.P("In this section we explore a more general nonlinear model, namely a random forest. The main purpose of this model is to offer more nuanced insight into the structure of the data. Random forest-type models were tuned by means of a randomized, cross-validated grid search. In this procedure parameters are randomly sampled from specified distributions, and the combination of parameters that scores best in cross-validation is chosen as the final configuration. As this is a computationally intensive procedure, we employed cloud technologies to perform it. Out-of-sample performance metrics like R squared and MSE were calculated on a test set comprising of 20% of the original data."),
                html.P("The importances are computed by randomly scrambling (permuting) one feature at a time, and seeing how much that increases the MSE of the model on a test set. In this way, it provides insight into how much each variable contributes to achieving good predictions. Our first observation is that hour is by far the most important determinant of noise, followed by the effect of weekday. Out of the weather variables, temperature plays the biggest role, though only risking an increase of 0.07 MSE."),

            ],
            style={'margin-bottom': '20px'}
        ),
        html.Div(
            [
                html.Div(style={'flex': '10%'}),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='imp-plot-id',
                            figure=fig1,
                            style={'width': '100%', 'height': '100%'},
                        ),
                    ],
                    style={'flex': '45%', 'display': 'inline-block'}
                ),
                html.Div(
                    children=[
                        html.Label('Select between the day model and night only model', style={'font-size': '25px'}),
                        dcc.RadioItems(
                            id='radio-item-daynight',
                            options=[
                                {'label': 'Day', 'value': 'option-day'},
                                {'label': 'Night (11PM - 6AM)', 'value': 'option-night'},
                            ],
                            value='option-day',
                            labelStyle={'display': 'block','margin-top':'10px','font-size': '20px'}
                        ),
                        html.Div(id='radio-item-caption',style={"margin-top":"40px"})
                    ],
                    style={'flex': '45%', 'margin': '30px', 'vertical-align': 'top', 'display': 'inline-block'}
                ),
                html.Div(style={'flex': '10%'})
            ],
            style={'display': 'flex', 'height': '450px', 'width': '100%'}
        ),
        html.Div(
            children=[
                html.P("Due to the overwhelming effect of the 24-hour cycle, we trained and tuned a separate random forest containing only nightly hours, here defined as the 8-hour window between 11PM to 6AM inclusive. It is interesting how the importance of other variables changes at night. Friday, the typical party night in Leuven, suddenly becomes much more important. Nightly temperature and rainfall also play a bigger role, suggesting that the effect depends on the presence of people, who may base their decision of being outside on the weather. In the same vein, KUL holidays are now more important, suggesting that these people present are at least in part students."),
                html.Br(),
                html.H3("Individual effects",style={"margin-left":"100px"}),
                html.P("Using partial dependence plots, we can estimate the effect of one predictor on the outcome while all the other predictors are kept constant. We show the most influential weather variables over the whole day:")

            ],
            style={'margin-top': '50px'}
        ),
        html.Div(
            [
                html.Div(style={'flex': '10%'}),
                     html.Div(
            children=[
          dcc.Graph(
            id='depen-plot-id',
            figure=fig2,
            style={'width': '800px', 'height': '100%', 'margin-left': '148px'},
          ),
        ],
        style={'display': 'inline-block', 'justify-content': 'center', 'align-items': 'center'}
      ),
html.Div(
                    children=[
                        html.Label('Select feature', style={'font-size': '25px'}),
                        dcc.RadioItems(
                            id='radio-item-predictor',
                            options=[
                                {'label': 'Temperature', 'value': 'option-temp'},
                                {'label': 'Rain', 'value': 'option-rain'},
                                {'label': 'Windspeed', 'value': 'option-windspeed'},
                            ],
                            value='option-temp',
                            labelStyle={'display': 'block','margin-top':'10px','font-size': '20px'}
                        ),
    html.Div(id='radio-item-name',style={"margin-top":"40px"})
    ],
    style={'flex': '10%', 'margin': '30px', 'vertical-align': 'top', 'display': 'inline-block'}
  ),
html.Div(
            children=[
                html.P("The effects of the weather variables are relatively small but measurable. Also keep in mind that the decibel scale is a logarithmic scale, meaning that it expresses multiplicative effects in loudness. For example, a sound that is 10 times more intense than another sound would be represented as a difference of 10 decibels on the scale. This means that even a change in average noise level of a decibel or less attributed to a feature can be a significant finding. In the partial dependences, we see that similarly to the bivariate case, temperature displays an inverse U-curve where noise is mostly high during medium temperatures. We suspect this is because the seasons in which nightlife and social life are most active in Leuven occur in medium temperature, since both the winter and summer are exam periods. Moreover, noise increases with windspeed and rain, presumably because these phenomena themselves make noise."),
                html.Br(),
                html.H3("Categorical effects",style={"margin-left":"100px"}),
                html.P("For the individual effects of the categorical variables, we simply plot their effect on estimated sound level, again holding all other features constant. This way we uncover their effect on the prediction in decibels"),

            ],
            style={'margin-top': '50px'}
),
html.Div(
                    children=[
                        dcc.Graph(
                            id='catimp-plot-id',
                            figure=fig3,
                            style={'height': '100%', 'width': '600px'},
                        ),
                    ],
            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                ),
html.Div(
            children=[
                html.P("The categorical variables show a pattern of being quieter on the weekends and on holidays, but now we can attach exact effect sizes to these patterns. A public holiday seems to decrease to predicted noise level by about the same level as a monday, while a KUL holiday's dampening effect is comparable to that of a saturday. Sunday has the largest effect, diminishing the noise level by more than 2 full decibels."),
                html.Br(),
                html.H3("The effect of hour",style={"margin-left":"100px"}),
                html.P("Due to the cyclical encoding of hour, we can actually display the hour effects on a unit circle by plotting the joint dependence of hour_sin and hour_cos. The effect of hour can be seen as following the perimeter of the unit circle representing 24 hours as annotated on the figure. Our model finds a clear day-night cycle with day in yellow, night in purple, and morning/evening between the two. From the angles in the plot we can derive that the model identifies the noisiest part of the day as starting on 9:45AM and ending at 8PM. The quietest part of the night is between 1:45AM and 5:20AM. The difference between the quietest and loudest predictions is almost a full 7 dB, indicating why hour is such an important variable.")

            ],
            style={'margin-top': '50px'}
),
                html.Div(
                    children=[
                        html.Img(src="assets/hourplot.jpg", style={'max-width': '40%', 'width': '500px' })
                    ],
                    style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-top': '20px'}
                )
        ]
        )
    ]
)




#########################################################################################################
# CALLBACK UPDATE FIGURE

@callback(
    [Output('imp-plot-id', 'figure'),
     Output('radio-item-caption', 'children')],
    [Input('radio-item-daynight', 'value')],
)
def update_figure(sel):
    text=""

    if(sel=="option-day"):
        modelsel = dayimportances
        text = f"MSE: {MSEday}\nR\u00b2: {r2day}"
    elif(sel=="option-night"):
        modelsel = nightimportances
        text = f"MSE: {MSEnight}\nR\u00b2: {r2night}"

    feature_names = modelsel.index.tolist()
    importances = np.ravel(modelsel)

    fig_updated = go.Figure()
    fig_updated.add_trace(go.Bar(
        x=importances,
        y=feature_names,
        orientation='h',
        marker=dict(color="#E6AF2E"),
        hovertemplate='<b>Feature:</b> %{y}<br>' +
                        '<b>Mean MSE increase:</b> %{x:.2f}<extra></extra>'
    ))

    fig_updated.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        title=dict(text='Random forest permutation feature importance', font=dict(color="white", size=24)),
        xaxis_title='Mean MSE increase',
        yaxis_title='Feature name',
        yaxis=dict(showgrid=True, zeroline=True, gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),tickfont=dict(color="white"),),
        xaxis=dict(showgrid=True, zeroline=True,  gridcolor='rgba(255, 255, 255, 0.1)',title_font=dict(color="white", size =18),tickfont=dict(color="white"),),
        bargap=0.1,  # Set the gap between bars to 0.1 (adjust as needed)
        margin=dict(l=0, r=20, t=40, b=0)  # Set all margins to 0
    )

    return fig_updated, html.P(text, style={'white-space': 'pre-line','margin':'0'})

# Callback to update 2nd figure
@callback(
    [Output('depen-plot-id', 'figure'),
     Output('radio-item-name', 'children')],
    [Input('radio-item-predictor', 'value')],
)
def update_figure2(sels):
    text=""
    modelsels = None
    valuesels = None

    if(sels=="option-temp"):
        modelsels = tempdep
        valuesels = tempval
        feature = "Temperature (°C)"
    elif(sels=="option-rain"):
        modelsels = raindep
        valuesels = rainval
        feature = "Rain (mm)"
    elif(sels == "option-windspeed"):
        modelsels = winddep
        valuesels = windval
        feature = "Windspeed (m/s)"

    values = np.ravel(valuesels)
    means = np.ravel(modelsels)

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
        margin=dict(l=0, r=20, t=40, b=0) 
    )

    return fig_updated, html.P(text, style={'white-space': 'pre-line','margin':'0'})