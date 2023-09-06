from flask import Flask
from dash import Dash, dcc, html, no_update, callback_context, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from ..layout import User_layout, Statistics_layout
from ..layout.tab import *
import requests
from datetime import datetime
import plotly.graph_objects as go

global_data = None


def register_callbacks(dash_app):
    @dash_app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
    )
    def render_page_content(pathname):
        if pathname == "/":
            return User_layout
        elif pathname == "/statistics":
            return Statistics_layout

    @dash_app.callback(
        [Output('user-image', 'src'),
         Output('chart-image', 'src')],
        [Input('url', 'pathname')]
    )
    def update_image_src(pathname):
        if pathname == "/":
            return "/assets/img/user_white.png", "/assets/img/chart_black.png"

        elif pathname == "/statistics":
            return "/assets/img/user_black.png", "/assets/img/chart_white.png"

    @dash_app.callback(
        Output('user-modify-button', 'style'),
        [Input('user-tabs', 'active_tab')]
    )
    def toggle_tab1_layout(tab_id):
        if tab_id == "user-tab-1":
            return {'display': 'block'}
        else:
            return {'display': 'none'}

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
            response = requests.get("http://192.9.200.45:8000/user/users")
            return response.json()

        if tab == 'user-tab-2' and n_clicks_2:
            url = f"http://192.9.200.45:8000/activity/{user_email_tab2}/{year_tab2}/{month_tab2}"
            response = requests.get(url)
            # print(response.json())
            return response.json()

        if tab == 'user-tab-3' and n_clicks_3:
            url = f"http://192.9.200.45:8000/activity/{user_email_tab3}/{year_tab3}/{month_tab3}/{day_tab3}"
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
            df.columns = df.columns.str.upper()
            df.insert(0, '#', range(1, len(df) + 1))

            table = dash_table.DataTable(
                id='user-information-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                sort_action='native',
                row_selectable='single',
                style_table={
                    'text-align': 'center',
                    'border-color': '#dee2e6'
                },
                style_header={  # 헤더 스타일링
                    'backgroundColor': 'lightgray',
                    'fontWeight': 'bold',
                },
                style_cell={  # 각 셀 스타일링
                    # 'border': 'none'
                },
                style_data_conditional=[
                    {
                        'if': {'state': 'selected'},  # 선택된 행에 대한 조건
                        'backgroundColor': 'inherit',  # 배경색 제거
                        'border': '1px solid lightgray'
                    }
                ]
            )

            return table

        elif tab == 'user-tab-2' and data:
            df = pd.DataFrame(data['activitys'])
            df.columns = df.columns.str.upper()
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return table

        elif tab == 'user-tab-3' and data:
            df = pd.DataFrame([data['activity_stats']])
            df.columns = df.columns.str.upper()
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return table

    @dash_app.callback(
        Output('selected-row-data', 'data'),
        [Input('user-information-table', 'selected_rows')],
        [State('user-information-table', 'data')]
    )
    def store_selected_row(selected_rows, all_data):
        if selected_rows:
            return all_data[selected_rows[0]]
        return {}

    @dash_app.callback(
        Output('user-info-modal', 'is_open'),
        [Input('user-modify-button', 'n_clicks'),
         Input('save-button', 'n_clicks')],
        [State('user-info-modal', 'is_open'),
         State('selected-row-data', 'data')]
    )
    def toggle_modal(n1, n2, is_open, selected_data):
        ctx = callback_context
        if not ctx.triggered:
            return is_open
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == "user-modify-button":
            # print(selected_data)
            # print("Open")
            return not is_open

        elif button_id == "save-button":
            # print("Close")
            return not is_open
        return is_open

    @dash_app.callback(
        Output('dummy-output', 'children'),
        Output('url-refresh', 'href'),
        [Input('user-info-modal', 'is_open'),
         Input('save-button', 'n_clicks')],
        [State('selected-row-data', 'data'),
         State('input-name', 'value'),
         State('input-email', 'value'),
         State('input-password', 'value')]
    )
    def send_request(is_open, n, selected_data, input_name, input_email, input_password):
        # print("send_request callback triggered")
        # print(selected_data)
        if not is_open and n and n > 0:
            url = f"http://192.9.200.45:8000/user/{selected_data['EMAIL']}"

            # 데이터 준비
            data = {
                "name": input_name,
                "email": input_email,
                "password": input_password
            }

            response = requests.put(url, json=data)

            if response.status_code == 200:
                return f"Request successful: {response.text}", '/'

        return "", None

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
            url = f"http://192.9.200.45:8000/activity/{user_email_tab1}/stats/{year_tab1}/{month_tab1}"
            response = requests.get(url)
            # print(response.json())
            return response.json()

        if tab == 'statistics-tab-2' and n_clicks_2:
            date_obj1 = datetime.strptime(start_date, '%Y-%m-%d')
            date_obj2 = datetime.strptime(end_date, '%Y-%m-%d')
            url = f"http://192.9.200.45:8000/activity/{user_email_tab2}/stats/{date_obj1.year}/{date_obj1.month}/{date_obj1.day}/{date_obj2.year}/{date_obj2.month}/{date_obj2.day}"
            response = requests.get(url)
            # print(response.json())
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
            df.columns = df.columns.str.upper()
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

            return table

        elif tab == 'statistics-tab-2' and data:
            df = pd.DataFrame(data['activity_stats'])
            df.columns = df.columns.str.upper()

            # 연도와 월을 합쳐서 새로운 'year_month' 열을 생성
            df['YEAR_MONTH'] = df['YEAR'].astype(str) + '-' + df['MONTH'].astype(str).str.zfill(2)
            df = df[['EMAIL', 'YEAR', 'MONTH', 'YEAR_MONTH', 'WARNING_COUNT', 'ACTIVITY_COUNT', 'FALL_COUNT']]

            # print(df)
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            color_palette = px.colors.qualitative.Pastel

            fig = go.Figure()

            # 각 카운트별로 바 추가
            fig.add_trace(go.Bar(x=df['YEAR_MONTH'], y=df['WARNING_COUNT'], name='Warning Count'))
            fig.add_trace(go.Bar(x=df['YEAR_MONTH'], y=df['ACTIVITY_COUNT'], name='Activity Count'))
            fig.add_trace(go.Bar(x=df['YEAR_MONTH'], y=df['FALL_COUNT'], name='Fall Count'))

            # fig.add_trace(go.Scatter(x=df['YEAR_MONTH'], y=df['WARNING_COUNT'], mode='lines', name='Warning Count'))
            # fig.add_trace(go.Scatter(x=df['YEAR_MONTH'], y=df['ACTIVITY_COUNT'], mode='lines', name='Activity Count'))
            # fig.add_trace(go.Scatter(x=df['YEAR_MONTH'], y=df['FALL_COUNT'], mode='lines', name='Fall Count'))

            # 차트의 레이아웃 설정 (옵션)
            fig.update_layout(barmode='group', title='Activity Statistics by Month', title_x=0.5, template="plotly_white")
            fig.update_xaxes(
                title="Year - Month",
                type='category'
            )
            fig.update_layout(
                font=dict(
                    family="Work Sans",
                    size=12,
                    color="black"
                )
            )

            return html.Div([
                table,
                dcc.Graph(figure=fig)
            ])
