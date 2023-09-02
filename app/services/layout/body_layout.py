from dash import dcc, html
import dash_bootstrap_components as dbc

from .tab import tab2_filter_layout, tab3_filter_layout

Home_layout = dbc.Container([

])

User_layout = dbc.Container([
    dcc.Store(id='store-data', storage_type='session'),  # 데이터 저장용
    dbc.Tabs(
        [
            dbc.Tab(label="유저 목록", tab_id="tab-1"),
            dbc.Tab(children=[tab2_filter_layout], label="특정 유저의 활동 목록 (년/월)", tab_id="tab-2"),
            dbc.Tab(children=[tab3_filter_layout], label="특정 유저의 활동 목록 (년/월/일)", tab_id="tab-3"),
        ],
        id="tabs",
        active_tab="tab-1",
    ),
    html.Div(id="tabs-content")
])

content_layout = html.Div(id="page-content", children=[])

body_layout = dbc.Container([
    content_layout
], className='CONTENT_STYLE')
