from flask import Flask
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

from ...component import *

user_tab1_filter_layout = dbc.Container([
    dbc.Row([
        dbc.Col(width=10),
        dbc.Col(
            dbc.Button([
                html.Div([
                    html.Img(src="/assets/img/change_white.png"),
                    html.Span("modify", className="filter-text"),
                ])
            ], id="user-modify-button", color="success", n_clicks=0, ), width=2, style={"padding-right": 0}
        )
    ]),
    dbc.Modal(
        [
            dcc.Store(id='selected-row-data'),
            dbc.ModalHeader("Modify User Information", style={"font-weight": "bold"}),
            dbc.ModalBody(
                [
                    dbc.Row([
                        dbc.Col(dbc.Label("Name:", className="mr-2"), width=4),
                        dbc.Col(dbc.Input(type="text", id="input-name"), width=8),
                    ], className="mb-2"),

                    dbc.Row([
                        dbc.Col(dbc.Label("Email:", className="mr-2"), width=4),
                        dbc.Col(dbc.Input(type="text", id="input-email"), width=8),
                    ], className="mb-2"),

                    dbc.Row([
                        dbc.Col(dbc.Label("Password:", className="mr-2"), width=4),
                        dbc.Col(dbc.Input(type="password", id="input-password"), width=8),
                    ], className="mb-2"),
                ]
            ),
            dbc.ModalFooter(
                dbc.Button("Save", id="save-button", className="ml-auto", color="success")
            ),
        ],
        id="user-info-modal", ),
    html.Div(id='dummy-output', style={'display': 'none'})
])

user_tab2_filter_layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(user_UserEmail_tab2, width=3, className="filter-content"),
            dbc.Col(user_year_tab2, width=2, className="filter-content"),
            dbc.Col(user_month_tab2, width=2, className="filter-content"),
            dbc.Col(width=3),
            dbc.Col(
                dbc.Button([
                    html.Div([
                        html.Img(src="/assets/img/filter.png"),
                        html.Span("Filter", className="filter-text"),
                    ])
                ], id="user-update-button-2", color="success"), width=1
            )
        ]),
    ],
)

user_tab3_filter_layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(user_UserEmail_tab3, width=3, className="filter-content"),
            dbc.Col(user_year_tab3, width=2, className="filter-content"),
            dbc.Col(user_month_tab3, width=2, className="filter-content"),
            dbc.Col(user_day_tab3, width=2, className="filter-content"),
            dbc.Col(width=1, style={"padding": 0}),
            dbc.Col(
                dbc.Button([
                    html.Div([
                        html.Img(src="/assets/img/filter.png"),
                        html.Span("Filter", className="filter-text"),
                    ])
                ], id="user-update-button-3", color="success"), width=1
            )
        ]),
    ],
)
