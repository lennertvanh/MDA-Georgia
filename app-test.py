import dash
from dash import dcc
from dash import html
#from dash.dependencies import Input, Output


app = dash.Dash(__name__, use_pages=True)

# Home Page
app.layout = html.Div([
    html.H1('Overview of the pages of the app'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']}".replace('-'," "), href=page["relative_path"]  # - {page['path']}
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

    html.Hr(style={'border-top': '1px solid black'}),

	dash.page_container
])


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