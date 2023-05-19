import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children='Welcome to the home page of the app'),

    html.Div(children='''
        Data about the city of Leuven will be analyzed and hopefully insight about it will be given.
    '''),

])