from flask import Flask
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

from app.services.component import *

tab2_filter_layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(UserEmail_tab2, width=3, className="filter-content"),
            dbc.Col(year_tab2, width=2, className="filter-content"),
            dbc.Col(month_tab2, width=2, className="filter-content"),
            dbc.Col(width=3),
            dbc.Col(
                dbc.Button([
                    html.Div([
                        html.Img(src="/assets/img/filter.png"),
                        html.Span("Filter", className="filter-text"),
                    ])
                ], id="update-button-2", color="success"), width=1
            )
        ]),
        html.Div(id='tab2-filtered-output')
    ],
)

tab3_filter_layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(UserEmail_tab3, width=3, className="filter-content"),
            dbc.Col(year_tab3, width=2, className="filter-content"),
            dbc.Col(month_tab3, width=2, className="filter-content"),
            dbc.Col(day_tab3, width=2, className="filter-content"),
            dbc.Col(width=1, style={"padding": 0}),
            dbc.Col(
                dbc.Button([
                    html.Div([
                        html.Img(src="/assets/img/filter.png"),
                        html.Span("Filter", className="filter-text"),
                    ])
                ], id="update-button-3", color="success"), width=1
            )
        ]),
        html.Div(id='tab3-filtered-output')
    ],
)
