from dash import dcc, html
import dash_bootstrap_components as dbc

# from app.services.layout.tab.user_tab import tab2_filter_layout, tab3_filter_layout
from .tab.user_tab import *
from .tab.statistics_tab import *

User_layout = dbc.Container([
    dcc.Location(id='url-refresh', refresh=True),
    dcc.Store(id='user-store-data', storage_type='session'),
    dbc.Tabs(
        [
            dbc.Tab(label="유저 목록", tab_id="user-tab-1"),
            dbc.Tab(children=[user_tab2_filter_layout], label="특정 유저의 활동 목록 (년/월)", tab_id="user-tab-2"),
            dbc.Tab(children=[user_tab3_filter_layout], label="특정 유저의 활동 목록 (년/월/일)", tab_id="user-tab-3"),
        ],
        id="user-tabs",
        active_tab="user-tab-1",
    ),
    html.Div(id="user-tabs-content"),
    user_tab1_filter_layout
])

Statistics_layout = dbc.Container([
    dcc.Store(id='statistics-store-data', storage_type='session'),
    dbc.Tabs(
        [
            dbc.Tab(children=[statistics_tab_filter_layout], label="특정 유저의 활동 통계 (년/월)", tab_id="statistics-tab-1"),
            dbc.Tab(children=[statistics_tab2_filter_layout], label="특정 유저의 활동 통계 (기간)", tab_id="statistics-tab-2"),
        ],
        id="statistics-tabs",
        active_tab="statistics-tab-1",
    ),
    html.Div(id="statistics-tabs-content")
])

content_layout = html.Div(id="page-content", children=[])

body_layout = dbc.Container([
    content_layout
], className='CONTENT_STYLE')
