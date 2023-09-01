from flask import Flask
from dash import Dash, dcc, html, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

from .layout import main_layout

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
server = Flask(__name__)
dash = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
dash.layout = main_layout


@dash.callback(
    Output('output-date-range', 'children'),
    [Input('component-date-picker-range', 'start_date'),
     Input('component-date-picker-range', 'end_date'),
     Input('update-button', 'n_clicks')]
)
def update_output_range(start_date, end_date, n_clicks):
    if n_clicks is not None:
        return f"Selected range: {start_date} to {end_date}"
    return no_update


@dash.callback(
    Output('output-email', 'children'),
    [Input('component-user-email', 'value')]
)
def update_output_email(value):
    return f"User email: {value}"


# Flask routes
@server.route('/')
def index():
    return "Flask App - Go to /dashboard for the dashboard"


@server.route('/dashboard')
def render_dashboard():
    return dash.index()


# Run the app
if __name__ == '__main__':
    server.run(debug=True)
