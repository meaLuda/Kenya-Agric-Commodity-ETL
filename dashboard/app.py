import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
from sqlalchemy import create_engine
import logging
import plotly.graph_objects as go


from dash.dependencies import Input, Output
from pages.home import (
    home_page,map_page,data_page,time_series_page
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
# app.config.suppress_callback_exceptions=True
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow": "auto",
    "transition": "margin-left 0.5s",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.Div([
            html.P("Kenya Agriculture Commodity Insights", className="display-4 ml-3 mt-4 mb-4"),
            html.Hr(),
            html.P(
                "An extensive analytics dashboard using "
                "data from different sources on Kenya's Agricultural Sector",
                className="lead",
            ),
        ]),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Data View", href="/data-view", active="exact"),
                dbc.NavLink("Time Series", href="/time-series", active="exact"),
                dbc.NavLink("About", href="/About", active="exact"),
                # dbc.NavLink("Summary-Analytics", href="/Summary-Analytics", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)
# Database connection
# engine = create_engine('postgresql://username:password@localhost:5432/yourdatabase')
engine = create_engine('postgresql://postgres:RQaoNj7QEDxq@localhost:5433/Kemis_analytics_db')

# Toggle button to show/hide sidebar
toggle_button = html.Button(
    html.Span(className="navbar-toggler-icon"),
    className="navbar-toggler",
    style={"position": "absolute", "left": "1rem", "top": "1rem"},
    id="toggle-button",
)

app.layout = html.Div([toggle_button, dcc.Location(id="url"), sidebar, content])


# Callback to toggle sidebar
@app.callback(Output("sidebar", "style"),[Input("toggle-button", "n_clicks")],prevent_initial_call=True)
def toggle_sidebar(n):
    if n and n % 2 == 1:
        return {"margin-left": "-20rem"}
    else:
        return SIDEBAR_STYLE

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return map_page.MAP_LAYOUTS
    elif pathname == "/data-view":
        return data_page.DATA_PAGE
    elif pathname == "/time-series":
        return time_series_page.TIME_SERIES_PAGE
    elif pathname == "/About":
        return home_page.home_page_content
    # elif pathname == "/Summary-Analytics":
    #     return summaryReport.layout
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),
        ],
        className="p-3 bg-light rounded-3",
    )





if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=3000)
