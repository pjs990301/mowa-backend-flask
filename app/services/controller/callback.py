from flask import Flask
from dash import Dash, dcc, html, no_update, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from ..layout import User_layout, Statistics_layout
import requests
from datetime import datetime

global_data = None


def register_callbacks(dash_app):
    @dash_app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
    )
    def render_page_content(pathname):
        if pathname == "/":
            return [html.H1('Home',
                            style={'textAlign': 'center'}), ]
        elif pathname == "/user":
            return User_layout

        elif pathname == "/statistics":
            return Statistics_layout

    @dash_app.callback(
        Output('user-store-data', 'data'),
        [Input('user-tabs', 'active_tab'),
         Input('user-update-button-2', 'n_clicks'),
         Input('user-update-button-3', 'n_clicks')],
        [State('component-user-email-tab2', 'value'),
         State('component-user-email-tab3', 'value'),
         State('component-user-year-tab2', 'value'),
         State('component-user-year-tab3', 'value'),
         State('component-user-month-tab2', 'value'),
         State('component-user-month-tab3', 'value'),
         State('component-user-day-tab3', 'value'), ]
    )
    def fetch_data(tab, n_clicks_2, n_clicks_3,
                   user_email_tab2, user_email_tab3,
                   year_tab2, year_tab3,
                   month_tab2, month_tab3,
                   day_tab3):
        if tab == 'user-tab-1':
            response = requests.get("http://127.0.0.1:5000/user/users")
            return response.json()

        if tab == 'user-tab-2' and n_clicks_2:
            url = f"http://127.0.0.1:5000/activity/{user_email_tab2}/{year_tab2}/{month_tab2}"
            response = requests.get(url)
            # print(response.json())
            return response.json()

        if tab == 'user-tab-3' and n_clicks_3:
            url = f"http://127.0.0.1:5000/activity/{user_email_tab3}/{year_tab3}/{month_tab3}/{day_tab3}"
            response = requests.get(url)
            # print(response.json())
            return response.json()

        return {}

    @dash_app.callback(
        Output('user-tabs-content', 'children'),
        [Input('user-tabs', 'active_tab'),
         Input('user-store-data', 'data')]  # 여기서 데이터를 가져옵니다.
    )
    def update_content(tab, data):
        if tab == 'user-tab-1' and data:
            df = pd.DataFrame(data['users'])
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return table

        elif tab == 'user-tab-2' and data:
            df = pd.DataFrame(data['activitys'])
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return table

        elif tab == 'user-tab-3' and data:
            df = pd.DataFrame([data['activity_stats']])
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return table

    @dash_app.callback(
        Output('statistics-store-data', 'data'),
        [Input('statistics-tabs', 'active_tab'),
         Input('statistics-update-button-1', 'n_clicks'),
         Input('statistics-update-button-2', 'n_clicks')],
        [State('component-statistics-email-tab1', 'value'),
         State('component-statistics-year-tab1', 'value'),
         State('component-statistics-month-tab1', 'value'),
         State('component-statistics-email-tab2', 'value'),
         State('component-statistics-date-picker-range', 'start_date'),
         State('component-statistics-date-picker-range', 'end_date'),

         ]
    )
    def fetch_statistics_data(tab, n_clicks_1, n_clicks_2, user_email_tab1, year_tab1, month_tab1, user_email_tab2,
                              start_date, end_date):
        if tab == 'statistics-tab-1' and n_clicks_1:
            url = f"http://127.0.0.1:5000/activity/{user_email_tab1}/stats/{year_tab1}/{month_tab1}"
            response = requests.get(url)
            print(response.json())
            return response.json()

        if tab == 'statistics-tab-2' and n_clicks_2:
            date_obj1 = datetime.strptime(start_date, '%Y-%m-%d')
            date_obj2 = datetime.strptime(end_date, '%Y-%m-%d')
            url = f"http://127.0.0.1:5000/activity/{user_email_tab2}/stats/{date_obj1.year}/{date_obj1.month}/{date_obj1.day}/{date_obj2.year}/{date_obj2.month}/{date_obj2.day}"
            response = requests.get(url)
            print(response.json())
            return response.json()

        return {}

    @dash_app.callback(
        Output('statistics-tabs-content', 'children'),
        [Input('statistics-tabs', 'active_tab'),
         Input('statistics-store-data', 'data')]
    )
    def update_statistics_content(tab, data):
        if tab == 'statistics-tab-1' and data:
            df = pd.DataFrame([data['activity_stats']])
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return table

        elif tab == 'statistics-tab-2' and data:
            df = pd.DataFrame([data['activity_stats']])
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return table
