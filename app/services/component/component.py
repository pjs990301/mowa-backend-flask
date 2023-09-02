from flask import Flask
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

'''
Card component
'''
StartDatePicker = dcc.DatePickerSingle(
    id='component-start-date-picker',
    placeholder="Start Period",
)

EndDatePicker = dcc.DatePickerSingle(
    id='component-end-date-picker',
    placeholder="End Period",
)

UserEmail_tab2 = dbc.Input(
    id='component-user-email-tab2',
    placeholder="Input your email",
    type="text",
)

year_tab2 = dbc.Input(
    id='component-user-year-tab2',
    placeholder="year",
    type="number",
    min=0, step=1
)

month_tab2 = dbc.Input(
    id='component-user-month-tab2',
    placeholder="month",
    type="number",
    min=1, max=12, step=1
)

UserEmail_tab3 = dbc.Input(
    id='component-user-email-tab3',
    placeholder="Input your email",
    type="text",
)

year_tab3 = dbc.Input(
    id='component-user-year-tab3',
    placeholder="year",
    type="number",
    min=0, step=1
)

month_tab3 = dbc.Input(
    id='component-user-month-tab3',
    placeholder="month",
    type="number",
    min=1, max=12, step=1
)

day_tab3 = dbc.Input(
    id='component-user-day-tab3',
    placeholder="day",
    type="number",
    min=1, max=31, step=1
)
