import dash
from dash import html, dcc, callback
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.graph_objects as go

dash.register_page(__name__)

#from kmi for Leuven from 1991 to 2020
#https://www.meteo.be/nl/klimaat/klimaat-van-belgie/klimaat-in-uw-gemeente
avg_rain_month = [70.4, 62.2, 54.4, 43.3, 55.5, 67.3, 72.7, 79.5, 60.5, 62.8, 68.5, 83.5 ]

weather_data = pd.read_csv("Data for visualization/daily_weatherdata_2022.csv")

weather_data["LC_DAILYRAIN_mm"] = weather_data["LC_DAILYRAIN"]*1000  #have in mm instead of m
total_rain_per_month = weather_data.groupby("Month")["LC_DAILYRAIN_mm"].sum()

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


#############################################################################################################""
#figure 1
# Create the scatter plots
fig1 = go.Figure()

# Add the scatter plot for average rainfall over the last 20 years
fig1.add_trace(go.Scatter(x=months, y=avg_rain_month, name="Average Rainfall (Last 20 Years)", mode="markers+lines", marker=dict(color='#2A9D8F'), line=dict(color='#2A9D8F')))

# Add the scatter plot for rainfall in 2022
fig1.add_trace(go.Scatter(x=months, y=total_rain_per_month, name="Rainfall in 2022", mode="markers+lines", marker=dict(color='#EB862E'), line=dict(color='#EB862E')))

# Update the layout
fig1.update_layout(
    title=dict(text="Rainfall comparison between year 2022 and the average over the past 20 years", 
               x=0.5,
               font=dict(color="white", size=24)
               ),
    xaxis=dict(title='Month',
               showgrid=True,
               zeroline=True,
               gridcolor='rgba(255, 255, 255, 0.1)',
               title_font=dict(color="white", size=18)),
    yaxis=dict(title='Rainfall (mm)',
               showgrid=True,
               zeroline=True,
               gridcolor='rgba(255, 255, 255, 0.1)',
               title_font=dict(color="white", size=18)),
    plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
    paper_bgcolor='rgba(0,0,0,0)'  # Set the paper background color to transparent
)
fig1.update_xaxes(color="white", gridwidth=2)
fig1.update_yaxes(color="white")
fig1.update_traces(hovertemplate='%{x}: %{y:.1f}°C', hoverlabel=dict(namelength=0))

# Text of the legend in white
fig1.update_layout(
    legend=dict(
        font=dict(color='white')
    )
)




######################################################################################################""
#figure 2

cutoff_rain_day = 0.0002

weather_data["bool_rainday"] = weather_data["LC_DAILYRAIN"] > cutoff_rain_day

rainy_counts = weather_data.groupby('Month')['bool_rainday'].sum()  # Count the number of rainy days per month


# Create the bar chart
fig2 = go.Figure(data=go.Bar(x=months, y=rainy_counts))

# Set the color of bars to yellow
fig2.update_traces(marker=dict(color='#E6AF2E'))
fig2.update_traces(hovertemplate='%{x}: %{y}', hoverlabel=dict(namelength=0))

# Customize the chart layout
fig2.update_layout(
    title=dict(text="Number of rainy days per month", x=0.5, font=dict(color="white")),
    xaxis_title="Month",
    yaxis_title="Number of rainy days", 
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
    ),
    plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
    paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background color to transparent
)
fig2.update_xaxes(color="white",gridwidth=5)
fig2.update_yaxes(color="white")


######################################################################################################
#figure 3
#measured by kmi for leuven from 1991 to 2020
avg_temp_Uccle = [3.9, 4.4, 7.2, 10.4, 14.1, 17.1, 19.2, 18.8, 15.5, 11.6, 7.4, 4.5]

avg_temp_per_month = weather_data.groupby("Month")["LC_TEMP_QCL3"].mean()
# Create the scatter plots
fig3 = go.Figure()

# Add the scatter plot for average rainfall over the last 20 years
fig3.add_trace(go.Scatter(x=months, y=avg_temp_Uccle, name="Average temperature (Last 20 Years)", mode="markers+lines", marker=dict(color='#2A9D8F'), line=dict(color='#2A9D8F')))

# Add the scatter plot for rainfall in 2022
fig3.add_trace(go.Scatter(x=months, y=avg_temp_per_month, name="Temperature in 2022", mode="markers+lines", marker=dict(color='#EB862E'), line=dict(color='#EB862E')))

# Update the layout
fig3.update_layout(
    title=dict(text="Temperature comparison between year 2022 and the average over the past 20 years", 
               x=0.5,
               font=dict(color="white", size=24)
               ),
    xaxis=dict(title='Month',
               showgrid=True,
               zeroline=True,
               gridcolor='rgba(255, 255, 255, 0.1)',
               title_font=dict(color="white", size=18)),
    yaxis=dict(title='Temperature (°C)',
               showgrid=True,
               zeroline=True,
               gridcolor='rgba(255, 255, 255, 0.1)',
               title_font=dict(color="white", size=18)),
    plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
    paper_bgcolor='rgba(0,0,0,0)'  # Set the paper background color to transparent
)
fig3.update_xaxes(color="white", gridwidth=2)
fig3.update_yaxes(color="white")
fig3.update_traces(hovertemplate='%{x}: %{y:.1f}mm', hoverlabel=dict(namelength=0))

# Text of the legend in white
fig3.update_layout(
    legend=dict(
        font=dict(color='white')
    )
)

##################################################################################""
#figure 4
#difference in temperature
diff_temp = avg_temp_per_month-avg_temp_Uccle

# Define colors based on diff_temp values
colors = ['#EB862E' if temp > 0 else '#2A9D8F' for temp in diff_temp]

# Create bar chart using go.Bar
data = go.Bar(
    x=months,
    y=diff_temp,
    marker=dict(color=colors),
    showlegend=False
)

# Create layout
layout = go.Layout(
    title=dict(text='Temperature differences between the year 2022 and the past 20 years',
               x=0.5,
               font=dict(color="white", size=24)),
    xaxis=dict(title='Months',
               showgrid=True,
               zeroline=True,
               gridcolor='rgba(255, 255, 255, 0.1)',
               title_font=dict(color="white", size=18)),
    yaxis=dict(title='Difference in temperature (°C)',
               showgrid=True,
               zeroline=True,
               gridcolor='rgba(255, 255, 255, 0.1)',
               title_font=dict(color="white", size=18)),
    plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color to transparent
    paper_bgcolor='rgba(0,0,0,0)'  # Set the paper background color to transparent
)

# Create figure
fig4 = go.Figure(data=[data], layout=layout)
fig4.update_xaxes(color="white",gridwidth=5)
fig4.update_yaxes(color="white")
fig4.update_traces(hovertemplate='%{x}: %{y:.1f}°C', hoverlabel=dict(namelength=0))

# Add legend items
fig4.add_trace(go.Scatter(
    x=[None],
    y=[None],
    mode='markers',
    marker=dict(color='#EB862E'),
    name='2022 warmer than average',
    showlegend=True
))
fig4.add_trace(go.Scatter(
    x=[None],
    y=[None],
    mode='markers',
    marker=dict(color='#2A9D8F'),
    name='2022 colder than average',
    showlegend=True
))

# Text of the legend in white
fig4.update_layout(
    legend=dict(
        font=dict(color='white')
    )
)



##################################################################################################################
# layout
layout = html.Div([
    html.H2("Weather Analysis"),
    html.P("In this page, we will inspect the weather in Leuven in 2022. Please select with the dropdown menu what you want to take a closer look at."), 
    html.Div(
        dcc.Dropdown(
            className="dropdown-style",
            id="figure-dropdown",
            searchable=False,
            clearable=False,
            options=[
                {"label": "How does the rainfall in 2022 compare to the past?", "value": "figure1"},
                {"label": "How much rainy days were there in each month of 2022?", "value": "figure2"},
                {"label": "How does the temperature in 2022 compare to the past?", "value": "figure3"},
                {"label": "Which months of 2022 were warmer or colder than the past?", "value": "figure4"}
            ],
            value="figure1",
            style={'background-color': '#223164'}
        ),
        #className="dropdown-style"
    ),
    html.Div(id="figure-container")
])

@callback(
    Output("figure-container", "children"),
    [Input("figure-dropdown", "value")]
)
def update_figure(selected_figure):
    if selected_figure == "figure1":
        return dcc.Graph(figure=fig1)
    elif selected_figure == "figure2":
        return dcc.Graph(figure=fig2)
    elif selected_figure == "figure3":
        return dcc.Graph(figure=fig3)
    elif selected_figure == "figure4":
        return dcc.Graph(figure=fig4)