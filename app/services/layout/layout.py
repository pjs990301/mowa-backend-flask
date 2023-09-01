from flask import Flask
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

from ..controller import controls_card

# Dash layout
main_layout = dbc.Container(
    [
        html.Div(id='Top-Head', children='MoWA Data Dashboard',
                style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
        dbc.Row([
            dbc.Col(controls_card, md=4),
            dbc.Col(
                [
                    dbc.Row([html.Div(id='output-date-range')], style={"marginBottom": "20px"}),
                    dbc.Row([html.Div(id='output-email')])
                ], md=8),

        ], align='center'),
    ],
    fluid=True
)
