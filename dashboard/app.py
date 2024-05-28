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
from pages.data_sources import sources
from pages.home import home_page,map_page,summaryReport

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
    "margin-left": "22rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.P("Kenya Agriculture Commodity Insights", className="display-4 ml-3 mt-4 mb-4"),
        html.Hr(),
        html.P(
            "An extensive analytics dashboard using "
            "data from different sources on Kenya's Agricultural Sector",
            className="lead",
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Data Sources", href="/d_sources", active="exact"),
                dbc.NavLink("About", href="/About", active="exact"),
                dbc.NavLink("Summary-Analytics", href="/Summary-Analytics", active="exact"),
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

# Load data
data = pd.read_sql_query("SELECT * FROM mv_market_summary_by_county_date", engine)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return map_page.layout
    elif pathname == "/d_sources":
        return sources.data_sources_content
    elif pathname == "/About":
        return home_page.home_page_content
    elif pathname == "/Summary-Analytics":
        return summaryReport.layout
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),
        ],
        className="p-3 bg-light rounded-3",
    )








# Callback to populate commodity dropdown
# @app.callback(
#     Output('commodity-dropdown', 'options'),
#     Input('commodity-dropdown', 'search_value')
# )
# def set_commodity_options(search_value):
#     query = "SELECT id, commodity FROM dim_commodity"
#     df = pd.read_sql(query, engine)
#     options = [{'label': row['commodity'], 'value': row['id']} for idx, row in df.iterrows()]
#     return options

# # Callback to populate market dropdown
# @app.callback(
#     Output('market-dropdown', 'options'),
#     Input('market-dropdown', 'search_value')
# )
# def set_market_options(search_value):
#     query = "SELECT id, market FROM dim_market"
#     df = pd.read_sql(query, engine)
#     options = [{'label': row['market'], 'value': row['id']} for idx, row in df.iterrows()]
#     return options

# Callback to update the time series chart based on selections
# @app.callback(
#     Output('kenya-timeseries', 'figure'),
#     [Input('commodity-dropdown', 'value'),
#      Input('market-dropdown', 'value'),
#      Input('date-picker-range', 'start_date'),
#      Input('date-picker-range', 'end_date')]
# )
# def update_timeseries(commodity_id, market_id, start_date, end_date):
#     print(f"Variables Incoming: \n Commodity id: {commodity_id} Market id: {market_id}\
#                   \n Start date: {start_date} End date: {end_date}")

#     if not commodity_id or not market_id or not start_date or not end_date:
#         # Return an empty figure if any of the inputs are not provided
#         return go.Figure()

#     query = f"""
#     SELECT dd.date, mp.wholesale_price, mp.retail_price, dm.market, dc.county
#     FROM fact_market_prices mp
#     JOIN dim_commodity dcom ON mp.commodity_sk = dcom.id
#     JOIN dim_market dm ON mp.market_sk = dm.id
#     JOIN dim_county dc ON mp.county_sk = dc.id
#     JOIN dim_date dd ON mp.date_sk = dd.id
#     WHERE dcom.id = {commodity_id} AND dm.id = {market_id} AND dd.date BETWEEN '{start_date}' AND '{end_date}'
#     ORDER BY dd.date
#     """
#     print(query)
#     df = pd.read_sql(query, engine)
#     print(df.head())
#     market = df['market'][0]
#     fig = px.line(df, x='date', y=['wholesale_price', 'retail_price'],
#                   labels={'value': 'Price', 'variable': 'Price Type'},
#                   title=f'Time Series of Prices for Commodity {commodity_id} in Market {market}')
#     fig.update_layout(xaxis_title='Date', yaxis_title='Price')
#     return fig





if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=3000)
