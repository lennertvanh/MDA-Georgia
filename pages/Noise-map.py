import dash
from dash import html, dcc, callback
import pandas as pd
import datetime
import plotly.graph_objects as go
from dash.dependencies import Input, Output  


dash.register_page(__name__)

## Data ##
noise_data = pd.read_csv("Data/hourly_noisedata_2022.csv")
