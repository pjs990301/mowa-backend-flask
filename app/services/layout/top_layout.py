from flask import Flask
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


top_layout = dbc.Container(
    [
        html.Div(id='Top-Head', children='MoWA Data Dashboard',
                 style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
    ],
    fluid=True, className='CONTENT_STYLE'
)