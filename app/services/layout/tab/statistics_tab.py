from ...component import *

statistics_tab_filter_layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(statistics_UserEmail_tab1, width=3, className="filter-content"),
            dbc.Col(statistics_year_tab1, width=2, className="filter-content"),
            dbc.Col(statistics_month_tab1, width=2, className="filter-content"),
            dbc.Col(width=3),
            dbc.Col(
                dbc.Button([
                    html.Div([
                        html.Img(src="/assets/img/filter.png"),
                        html.Span("Filter", className="filter-text"),
                    ])
                ], id="statistics-update-button-1", color="success"), width=1
            )
        ]),
    ],
)

statistics_tab2_filter_layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(statistics_UserEmail_tab2, width=3, className="filter-content"),
            dbc.Col(statistics_DateRange, width=4, className="filter-content"),
            dbc.Col(width=3),
            dbc.Col(
                dbc.Button([
                    html.Div([
                        html.Img(src="/assets/img/filter.png"),
                        html.Span("Filter", className="filter-text"),
                    ])
                ], id="statistics-update-button-2", color="success"), width=1
            )
        ]),
    ],
)
