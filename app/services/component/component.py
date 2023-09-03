from flask import Flask
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

user_UserEmail_tab2 = dbc.Input(
    id='component-user-email-tab2',
    placeholder="Input your email",
    type="text",
)

user_year_tab2 = dbc.Input(
    id='component-user-year-tab2',
    placeholder="year",
    type="number",
    min=0, step=1
)

user_month_tab2 = dbc.Input(
    id='component-user-month-tab2',
    placeholder="month",
    type="number",
    min=1, max=12, step=1
)

user_UserEmail_tab3 = dbc.Input(
    id='component-user-email-tab3',
    placeholder="Input your email",
    type="text",
)

user_year_tab3 = dbc.Input(
    id='component-user-year-tab3',
    placeholder="year",
    type="number",
    min=0, step=1
)

user_month_tab3 = dbc.Input(
    id='component-user-month-tab3',
    placeholder="month",
    type="number",
    min=1, max=12, step=1
)

user_day_tab3 = dbc.Input(
    id='component-user-day-tab3',
    placeholder="day",
    type="number",
    min=1, max=31, step=1
)

statistics_UserEmail_tab1 = dbc.Input(
    id='component-statistics-email-tab1',
    placeholder="Input your email",
    type="text",
)

statistics_year_tab1 = dbc.Input(
    id='component-statistics-year-tab1',
    placeholder="year",
    type="number",
    min=0, step=1
)

statistics_month_tab1 = dbc.Input(
    id='component-statistics-month-tab1',
    placeholder="month",
    type="number",
    min=1, max=12, step=1
)

statistics_UserEmail_tab2 = dbc.Input(
    id='component-statistics-email-tab2',
    placeholder="Input your email",
    type="text",
)

statistics_DateRange = dcc.DatePickerRange(
    id='component-statistics-date-picker-range',
    start_date_placeholder_text="Start Period",
    end_date_placeholder_text="End Period",
)
