from flask import Flask
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

'''
Card component
'''
DateRange = dcc.DatePickerRange(
    id='component-date-picker-range',
    start_date_placeholder_text="Start Period",
    end_date_placeholder_text="End Period",
)

UserEmail = dbc.Input(
    id='component-user-email',
    placeholder="Input your email",
    type="text"
)
