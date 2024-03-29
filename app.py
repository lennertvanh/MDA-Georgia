import dash
from dash import dcc
from dash import html
#from dash.dependencies import Input, Output


app = dash.Dash(__name__, use_pages=True)

# Home Page
app.layout = html.Div(
    [
        html.Div(
            className="app-header",
            children=[
                html.Div('Noise in The City of Leuven', className="app-header--title")
            ]
        ),
        html.Div(
            className="homepage-link-wrapper",
            style={"margin-top": "20px"},  # Add margin-top to the wrapper div
            children=[
                html.Div(
                    className="homepage-link",
                    style={
                        "border": "2px solid white",  # Add border
                        "padding": "10px",  # Add padding
                        "display": "inline-block"  # Set display to inline-block
                        },
                    children=[
                        dcc.Link("Homepage", href="/", style={"font-size": "20px", "font-weight": "bold"})
                    ]
                )
            ]
        ),
        html.Div(
            className="category-grid",
            children=[
                html.Div(
                    className="category-column",
                    children=[
                        html.H5("Explore the noise data"),  # Category 2: Analysis of Noise Levels
                        html.Div(
                            dcc.Link("Noise level over time", href="noise-level-over-time")
                        ),
                        html.Div(
                            dcc.Link("Noise level per month", href="noise-level-per-month")
                        ),
                        html.Div(
                            dcc.Link("Nightly noise peaks per location", href="spiderplots")
                        ),
                        html.Div(
                            dcc.Link("Noise level vs holidays", href="noise-level-vs-holidays")
                        ),
                        html.Div(
                            dcc.Link("Noise heatmap", href="noise-heatmap")
                        ),
                        html.Div(
                            dcc.Link("Noise events", href="noise-events")
                        ),
                        html.Div(
                            dcc.Link("Noise sources", href="noise-source-laeq")
                        ),
                         html.Div(
                            dcc.Link("Fourier transformation", href="fourier-transformation")
                        ),
                    ],
                    style={"margin-bottom": "20px"}  # Add margin-bottom for extra space
                ),
                html.Div(
                    className="category-column",
                    children=[
                        html.H5("Explore the weather data"),  # Category 3: Analysis of Weather
                        html.Div(
                            dcc.Link("Weather analysis", href="weather-analysis")
                        ),
                        html.Div(
                            dcc.Link("Wind plot", href="wind-plot")
                        ),
                    ],
                    style={"margin-bottom": "20px"}  # Add margin-bottom for extra space
                ),
                html.Div(
                    className="category-column",
                    children=[
                        html.H5("Analyzing noise and weather together"),  # Category 4: Analysis of Noise and Weather
                        html.Div(
                            dcc.Link("Effect of temperature on noise", href="noise-wrt-temp")
                        ),
                        html.Div(
                            dcc.Link("Effect of rain on noise", href="noise-level-dry-rainy-day")
                        ),
                        html.Div(
                            dcc.Link("Noise map", href="noise-map")
                        ),
                    ],
                    style={"margin-bottom": "20px"}  # Add margin-bottom for extra space
                ),
                html.Div(
                    className="category-column",
                    children=[
                        html.H5("Modelling"),  # Category 4: Analysis of Noise and Weather
                        html.Div(
                            dcc.Link("ARD regression", href="ard-regression")
                        ),
                        html.Div(
                            dcc.Link("Random forest", href="random-forest")
                        ),
                        html.Div(
                            dcc.Link("Traffic model", href="traffic-model")
                        ),
                        html.Div(
                            dcc.Link("XGB", href="xgb-modelling")
                        ),
                    ],
                    style={"margin-bottom": "20px"}  # Add margin-bottom for extra space
                ),
            ],
        ),
        html.Hr(style={"margin-top": "20px", "margin-bottom": "20px",'background-color':'rgba(19, 34, 68, 0.973)'}),  # Add horizontal line
        dash.page_container
    ],
    className="app-container"
)

if __name__ == '__main__':
    app.run_server(debug=True)


app.css.append_css({'external_url': 'assets/typography.css'})
app.css.append_css({'external_url': 'assets/header.css'})

server = app.server
