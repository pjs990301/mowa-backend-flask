from flask import Flask
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# from ..controller import controls_card

from .top_layout import top_layout
from .left_layout import sidebar_layout
from .body_layout import body_layout

main_layout = html.Div([
    dcc.Location(id="url"),
    sidebar_layout,
    top_layout,
    body_layout
])


