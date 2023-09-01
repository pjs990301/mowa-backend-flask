from flask import Flask
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

from ..component import DateRange, UserEmail

# Controls (Card)
controls_card = dbc.Card(
    [
        dbc.CardHeader("유저 검색"),

        dbc.CardBody(
            [
                html.H4("이메일", className="card-title"),
                html.Div(style={"margin-top": "10px", "margin-bottom": "10px"}),
                UserEmail
            ]
        ),

        dbc.CardBody(
            [
                html.H4("기간 설정", className="card-title"),
                html.Div(style={"margin-top": "10px", "margin-bottom": "10px"}),
                # DateRange,
                dbc.Row([
                    dbc.Col(DateRange, width=12),
                    dbc.Col(dbc.Button("Update", id="update-button", color="primary"), width=4)  # 버튼을 4의 너비로 설정
                ]),
            ]
        ),

    ],
    style={"width": "40%"}
)
