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
                html.Div('Noise Pollution in The City of Leuven', className="app-header--title")
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
                        html.H3("Explore the noise level data"),  # Category 2: Analysis of Noise Levels
                        html.Div(
                            dcc.Link("Noise level over time", href="noise-level-analysis")
                        ),
                        html.Div(
                            dcc.Link("Noise level per month", href="noise-level-per-month")
                        ),
                        html.Div(
                            dcc.Link("Noise events", href="noise-events")
                        ),
                        
                        html.Div(
                            dcc.Link("Noise heatmap", href="noise-heatmap")
                        ),
                        html.Div(
                            dcc.Link("Noise level vs holidays", href="noise-level-vs-holidays")
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
                        html.H3("Explore the weather data"),  # Category 3: Analysis of Weather
                        html.Div(
                            dcc.Link("Rain days per month", href="rain-days-per-month")
                        ),
                        html.Div(
                            dcc.Link("Rain overview plots", href="rain-overview-plots")
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
                        html.H3("Analyzing noise and weather together"),  # Category 4: Analysis of Noise and Weather
                        html.Div(
                            dcc.Link("Noise level in function dry rainy day", href="noise-level-in-function-dry-rainy-day")
                        ),
                        html.Div(
                            dcc.Link("Noise map test 3", href="noise-map-test-3")
                        ),
                    ],
                    style={"margin-bottom": "20px"}  # Add margin-bottom for extra space
                ),
            ],
        ),
        html.Hr(style={"margin-top": "20px", "margin-bottom": "20px"}),  # Add horizontal line
        dash.page_container
    ],
    className="app-container"
)



#@app.callback(Output('page-content', 'children'),
#              [Input('url', 'pathname')])
#def display_page(pathname):
#    if pathname == '/':
#        return app.layout
#    elif pathname == '/page-1':
#        return page_1_layout
#    else:
#        return '404 Page not found'

if __name__ == '__main__':
    app.run_server(debug=True)