from flask import Flask
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


sidebar_layout = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "Number of students per education level", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("User", href="/user", active="exact"),
                dbc.NavLink("Statistics/Chart", href="/statistics", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className='SIDEBAR_STYLE'
)
