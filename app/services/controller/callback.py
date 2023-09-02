from flask import Flask
from dash import Dash, dcc, html, no_update, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from ..layout import User_layout
import requests

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

    @dash_app.callback(
        Output('store-data', 'data'),
        [Input('tabs', 'active_tab'),
         Input('update-button-2', 'n_clicks'),
         Input('update-button-3', 'n_clicks')],
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
        if tab == 'tab-1':
            response = requests.get("http://127.0.0.1:5000/user/users")
            return response.json()

        if tab == 'tab-2' and n_clicks_2:
            url = f"http://127.0.0.1:5000/activity/{user_email_tab2}/{year_tab2}/{month_tab2}"
            response = requests.get(url)
            print(response.json())
            return response.json()

        if tab == 'tab-3' and n_clicks_3:
            url = f"http://127.0.0.1:5000/activity/{user_email_tab3}/{year_tab3}/{month_tab3}/{day_tab3}"
            response = requests.get(url)
            print(response.json())
            return response.json()

        return {}

    @dash_app.callback(
        Output('tabs-content', 'children'),
        [Input('tabs', 'active_tab'),
         Input('store-data', 'data')]  # 여기서 데이터를 가져옵니다.
    )
    def update_content(tab, data):
        if tab == 'tab-1' and data:
            df = pd.DataFrame(data['users'])
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return table

        elif tab == 'tab-2' and data:
            df = pd.DataFrame(data['activitys'])
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return table
        elif tab == 'tab-3' and data:
            df = pd.DataFrame([data['activity_stats']])
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return table
