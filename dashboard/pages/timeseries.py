# import dash
# from dash import html, dcc, callback, Input, Output
# import dash_bootstrap_components as dbc
# import plotly.express as px
# import pandas as pd
# from app import engine
# from statsmodels.tsa.seasonal import seasonal_decompose

# dash.register_page(__name__, path='/timeseries')

# layout = dbc.Container([
#     html.H1("Time Series Analysis", className="text-center mt-4"),
#     dbc.Row([
#         dbc.Col([
#             dcc.Dropdown(
#                 id='ts-commodity-dropdown-timeseries',
#                 options=[],
#                 value=None,
#                 placeholder="Select a commodity"
#             )
#         ], width=6),
#         dbc.Col([
#             dcc.Dropdown(
#                 id='ts-market-dropdown-timeseries',
#                 options=[],
#                 value=None,
#                 placeholder="Select a market"
#             )
#         ], width=6),
#     ], className="mt-4"),
#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id='ts-price-chart-timeseries')
#         ], width=12)
#     ], className="mt-4"),
#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id='ts-decomposition-chart-timeseries')
#         ], width=12)
#     ], className="mt-4"),
# ])

# @callback(
#     Output('ts-commodity-dropdown-timeseries', 'options'),
#     Input('ts-commodity-dropdown-timeseries', 'search_value')
# )
# def update_ts_commodity_options_timeseries(search_value):
#     query = "SELECT DISTINCT commodity FROM dim_commodity"
#     df = pd.read_sql(query, engine)
#     options = [{'label': c, 'value': c} for c in df['commodity']]
#     return options

# @callback(
#     Output('ts-market-dropdown-timeseries', 'options'),
#     Input('ts-market-dropdown-timeseries', 'search_value')
# )
# def update_ts_market_options_timeseries(search_value):
#     query = "SELECT DISTINCT market FROM dim_market"
#     df = pd.read_sql(query, engine)
#     options = [{'label': m, 'value': m} for m in df['market']]
#     return options

# @callback(
#     Output('ts-price-chart-timeseries', 'figure'),
#     Output('ts-decomposition-chart-timeseries', 'figure'),
#     Input('ts-commodity-dropdown-timeseries', 'value'),
#     Input('ts-market-dropdown-timeseries', 'value')
# )
# def update_ts_charts_timeseries(commodity, market):
#     if not commodity or not market:
#         return px.scatter(), px.scatter()

#     query = f"""
#     SELECT f.wholesale, f.retail, d.date
#     FROM fact_market_prices f
#     JOIN dim_commodity c ON f.commodity_id = c.commodity_id
#     JOIN dim_market m ON f.market_id = m.market_id
#     JOIN dim_date d ON f.date_id = d.date_id
#     WHERE c.commodity = '{commodity}' AND m.market = '{market}'
#     ORDER BY d.date
#     """
#     df = pd.read_sql(query, engine)
#     df.set_index('date', inplace=True)

#     price_fig = px.line(df, y=['wholesale', 'retail'],
#                         title=f"{commodity} Prices in {market} Market",
#                         labels={'value': 'Price', 'variable': 'Price Type'})

#     # Perform time series decomposition
#     decomposition = seasonal_decompose(df['wholesale'], model='additive', period=30)

#     decomp_fig = px.line(x=df.index, y=[decomposition.trend, decomposition.seasonal, decomposition.resid],
#                          title=f"Time Series Decomposition for {commodity} Wholesale Price in {market}",
#                          labels={'value': 'Component Value', 'variable': 'Component'})
#     decomp_fig.update_layout(legend_title_text='Component')

#     return price_fig, decomp_fig