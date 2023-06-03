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

coeff_full = pd.read_csv("Data for modelling/ARD_coefficients_train_full_data_with_split", index_col=0)

#without Vrijthof values
coeff_wo_Vrijt = pd.read_csv("Data for modelling/ARD_coefficients_train_data_without_Vrijthof_with_split", index_col=0)

#without Vrijthof values and without weekdays
coeff_wo_Vrijt_weekday = pd.read_csv("Data for modelling/ARD_coefficients_train_data_without_Vrijthof_with_split_without_weekday", index_col=0)

MSE_full = 0.603
r2_full = 0.397

MSE_wo_vrijt = 0.522
r2_wo_vrijt = 0.486

MSE_wo_vrijt_weekday = 0.563
r2_wo_vrijt_weekday = 0.446


#########################################################################################################
# VISUALIZATION

feature_names = coeff_full.index.tolist()
coefficients = np.ravel(coeff_full)

fig = go.Figure()
fig.add_trace(go.Bar(
    x=coefficients, #["coefficient"],  # Use the coefficient as the length of the bar
    y=feature_names, #["feature"],   # Use the coefficient name as the y-axis
    orientation='h', # Specify horizontal orientation
    marker=dict(
        color=np.where(coefficients < 0, 'red', 'green')
    )
))

fig.update_layout(
    title='Feature importance with ARD regression',
    xaxis_title='Coefficient',
    yaxis_title='Feature name',
    #width=400,  # Set the width of the plot to 800 pixels
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
                html.H2("ARD regression"),
                html.P("ARD regression is used on the data that was transformed into a highly dimensional dataset with 13 features about time, location and weather. The goal of the model is to predict the noise level in dB(A) given the time, location and weather. Ultimately, the purpose of the model is to determine the most important features influencing the noise level."),
                html.P("For curious or motivated readers, more explanation about the modelling is given below. In this section, only the conclusions will be given."),
                html.P("Using the full dataset, it can be observed that the most important features are the hour, the weekday and the coordinate in decreasing order of importance."),
                html.P("The data is analyzed a second time without the location 'Vrijthof' to see the influence on the feature coordinate that indicates the closeness to the center of Leuven. This analysis is done because the location Vrijthof is a kind of 'outlier' compared to the other locations, being very quiet compared to the other locations. This is confirmed as the feature 'coordinate' switches from sign when 'Vrijthof' is removed. The positive sign indicates now that it becomes noisier when we approach the center of Leuven."),
                html.P("In the third case, the feature 'weekday' is removed to see the influence on the feature 'day' as there could be some multicollinearity. Surprisingly, removing 'weekday' has almost no influence on the other coefficients. The regression model is simply less performant as the R squared reduced and the MSE increased."),
            ],
            style={'margin-bottom': '20px'}
        ),
        html.Div(
            [
                html.Div(style={'flex': '15%'}),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='coeff-plot-id',
                            figure=fig,
                            style={'width': '100%', 'height': '100%'},
                        ),
                    ],
                    style={'flex': '35%', 'display': 'inline-block'}
                ),
                html.Div(
                    children=[
                        html.Label('Select between the full dataset and truncated versions:', style={'font-size': '25px'}),
                        dcc.RadioItems(
                            id='radio-item-which-coeff',
                            options=[
                                {'label': 'With all the data and variables', 'value': 'option-full'},
                                {'label': 'Without Vrijthof', 'value': 'option-without-vrijthof'},
                                {'label': 'Without Vrijthof and weekday variable', 'value': 'option-without-vrijthof-weekday'},
                            ],
                            value='option-full',
                            labelStyle={'display': 'block','margin-top':'10px','font-size': '20px'}
                        ),
                        html.Div(id='radio-item-text',style={"margin-top":"40px"})
                    ],
                    style={'flex': '45%', 'margin': '30px', 'vertical-align': 'top', 'display': 'inline-block'}
                ),
                html.Div(style={'flex': '15%'})
            ],
            style={'display': 'flex', 'height': '450px', 'width': '100%'}
        ),
        html.Div(
            children=[   
                html.H3("What is ARD regression? How to interpret the coefficients?",style={"margin-left":"100px"}),
                html.P("ARD regression is closely related to Bayesian ridge regression. It is similar to a linear regression where the importance of the features can be determined thanks to the Bayesian framework. The absolute value of the coefficient indicates the importance of the feature. Moreover, the sign of the coefficient designates if there is a positive or negative correlation between the feature and the output variable."),
                html.H3("How is the model designed? Which features are used? And how are they defined?",style={"margin-left":"100px"}),
                html.P("Instead of using the data as a time-series that requires special models for this kind of data, the data is transformed to be able to use it with classical regression models. The time information is transformed into features 'month', 'day', 'hour' and 'weekday'."),
                html.P("The data is highly dimensional with 13 features for the 'full' model and contains over 55000 observations as the hourly dataset for all the locations has been used. The goal of the regression is to predict the sound level in dB(A) given information about the time, the location and the weather. All the features related to time are transformed with the sine and cosine of the value to incorporate the knowledge of time cycles. This means that the features 'month', 'day', 'hour' and 'weekday' become 'sin_month', 'cos_month', 'sin_day', 'cos_day', 'sin_hour','cos_hour', 'sin_weekday' and 'cos_weekday'."),
                html.P("The feature 'weekday' is a own created variable having a discrete value between 1 and 7 with '1' indicating 'Monday', '2' indicating 'Tuesday' and so on till 'Sunday' for weekday=7."),
                html.P("The variable 'coordiante' is another own created feature providing the 'spatial' information. To create the variable, the two extreme locations were selected, i.e. Naamsestraat 81 and Vrijthof. A virtual line was drawn between the two locations and all the other locations were projected on this virtual line. Naamsestraat 81 was assigned the value 0 and Vrijthof the value 1. This means that an increasing value in the coordinate indicates a location closer to the center of Leuven."),
                html.P("The feature 'month' is a discrete value between 1 and 12 indicating the month. Similarly, the feature 'day' gives the day of the month with a value between 1 and 31 (or 28/30 depending on the month). Finally, the feature 'hour' gives the hour of the day with a discrete value between 0 and 23."),
                html.P("Other features present in the data are the wind in m/s, the wind direction in degrees, the rain which is the amount of rain fallen during the hour and the average temperature in °C in the hour."),
                html.P("Concerning the cyclic features, they can be interpreted as following:"),
                html.P("- sin_month: A value close to one indicates the months of February, March and April. A value close to minus one indicate the months of August, September and October."),
                html.P("- cos_month: A value close to one indicates the months of November, December and January. A value close to minus one indicate the months of May, June and July."),
                html.P("- sin_day: Values close to one are days close to the 8th day of the month and negative values close to minus one are days close to the 22th day of the month."),
                html.P("- cos_day: A value close to one are days at the beginning of the month or at the end of the month. Negative values close to minus one are days close to the 15th day of the month."),
                html.P("- sin_hour: Positive values are all the hours before noon. Negative values are all the hours after noon."),
                html.P("- cos_hour: Positive values are hours when it is mainly dark outside (night). Negative values indicate hours where daylight is present."),
                html.P("- sin_weekday: Positive values are Monday, Tuesday and Wednesday. Negative values are Tuesday, Friday and Saturday."),
                html.P("- cos_weekday: Values close to one are Saturday, Sunday and Monday. Values close to minus one are Wednesday, Thursday and Friday in a lesser extendt."),
                html.H3("Training and test set?",style={"margin-left":"100px"}),
                html.P("The data is split into two subsets: the training and test sets with proportions 80-20. The training set is used to train the ARD model and get the coefficients. The test set is used to see how well the ARD regression performs on unseen data and is used to calculate the MSE and R squared."),
                html.H3("Interpretation of the most important features for the full model",style={"margin-left":"100px"}),
                html.P("The coefficient of 'cos_weekday' is highly negative indicating that Wednesday, Thursday and Friday are noisier than Saturday, Sunday and Monday. 'sin_hour' is highly negative meaning that it is noisier after noon than before noon. 'cos_hour' is also negative indicating that it is noisier during daylight than during the night which is expected as everyone is sleeping during the night. With the full dataset, 'coordinate' is negative which means that it becomes quieter when we get closer to the center. This is a surprising result as the opposite is expected. Probably that the negative sign is mainly due to Vrijthof being very quiet. When Vrijthof is removed, the opposite effect is observed, i.e. it becomes noisier when we get closer to the center.")
            ],
            style={'margin-top': '50px'}
        )
    ]
)


#########################################################################################################
# CALLBACK UPDATE FIGURE

@callback(
    [Output('coeff-plot-id', 'figure'),
     Output('radio-item-text', 'children')],
    [Input('radio-item-which-coeff', 'value')],
)
def update_figure(selected_coeff):
    text=""

    if(selected_coeff=="option-full"):
        coefficients_to_use = coeff_full
        text = f"MSE: {MSE_full}\nR\u00b2: {r2_full}"
    elif(selected_coeff=="option-without-vrijthof"):
        coefficients_to_use = coeff_wo_Vrijt
        text = f"MSE: {MSE_wo_vrijt}\nR\u00b2: {r2_wo_vrijt}"
    elif(selected_coeff=="option-without-vrijthof-weekday"):
        coefficients_to_use = coeff_wo_Vrijt_weekday
        text = f"MSE: {MSE_wo_vrijt_weekday}\nR\u00b2: {r2_wo_vrijt_weekday}"

    feature_names = coefficients_to_use.index.tolist()
    coefficients = np.ravel(coefficients_to_use)

    fig_updated = go.Figure()
    fig_updated.add_trace(go.Bar(
        x=coefficients, #["coefficient"],  # Use the coefficient as the length of the bar
        y=feature_names, #["feature"],   # Use the coefficient name as the y-axis
        orientation='h', # Specify horizontal orientation
        marker=dict(
            color=np.where(coefficients < 0, 'red', 'green')
        )
    ))

    fig_updated.update_layout(
        title='Feature importance with ARD regression',
        xaxis_title='Coefficient',
        yaxis_title='Feature name',
        #width=400,  # Set the width of the plot to 800 pixels
        bargap=0.1,  # Set the gap between bars to 0.1 (adjust as needed)
        margin=dict(l=0, r=20, t=40, b=0)  # Set all margins to 0
    )

    return fig_updated, html.P(text, style={'white-space': 'pre-line','margin':'0'})
