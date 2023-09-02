from flask import Flask
from dash import Dash, dcc, html, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

from .controller import register_callbacks
from .layout import main_layout

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
server = Flask(__name__)
dash = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css],
            suppress_callback_exceptions=True)

dash.layout = main_layout
register_callbacks(dash)

# Run the app
if __name__ == '__main__':
    server.run(debug=True, port=8050)
