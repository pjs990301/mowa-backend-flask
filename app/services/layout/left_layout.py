from flask import Flask
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

sidebar_layout = html.Div(
    [
        html.H2("Memu", className="Side-bar-title"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink([
                    html.Img(src="/assets/img/user_black.png", id="user-image",
                             style={'height': '20px', 'width': '20px', 'margin-right': '10px'}),
                    "User"
                ], href="/", active="exact"),
                dbc.NavLink([
                    html.Img(src="/assets/img/chart_black.png", id="chart-image",
                             style={'height': '20px', 'width': '20px', 'margin-right': '10px'}),
                    "Statistics / Chart"
                ], href="/statistics", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className='SIDEBAR_STYLE'
)
