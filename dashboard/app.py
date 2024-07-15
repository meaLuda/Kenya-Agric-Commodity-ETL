import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from sqlalchemy import create_engine
from dash.exceptions import PreventUpdate



# Create a connection to the analytics database
db_url = "postgresql://postgres:RQaoNj7QEDxq@localhost:5432/kemis_analytics_db"
engine = create_engine(db_url)

# Create the Dash app
app = dash.Dash(__name__,prevent_initial_callbacks = True, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)


### ----------------> Import pages
import pages.home
import pages.commodity
import pages.market
import pages.timeseries


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Commodity Analysis", href="/commodity")),
        # dbc.NavItem(dbc.NavLink("Market Trends", href="/market")),
        # dbc.NavItem(dbc.NavLink("Time Series", href="/timeseries")),
    ],
    brand="Agricultural Market Dashboard",
    brand_href="/",
    color="primary",
    dark=True,
)

app.layout = html.Div([
    navbar,
    dash.page_container
])


if __name__ == '__main__':
    app.run_server(debug=True)