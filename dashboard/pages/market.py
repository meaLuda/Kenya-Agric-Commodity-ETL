# import dash
# from dash import html, dcc, callback, Input, Output
# import dash_bootstrap_components as dbc
# import plotly.express as px
# import pandas as pd
# from app import engine

# dash.register_page(__name__, path='/market')

# layout = dbc.Container([
#     html.H1("Market Trends", className="text-center mt-4"),
#     dbc.Row([
#         dbc.Col([
#             dcc.Dropdown(
#                 id='market-dropdown-market',
#                 options=[],
#                 value=None,
#                 placeholder="Select a market"
#             )
#         ], width=6),
#         dbc.Col([
#             dcc.Dropdown(
#                 id='commodity-multi-dropdown-market',
#                 options=[],
#                 value=[],
#                 multi=True,
#                 placeholder="Select commodities"
#             )
#         ], width=6),
#     ], className="mt-4"),
#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id='market-comparison-chart-market')
#         ], width=12)
#     ], className="mt-4"),
# ])

# @callback(
#     Output('market-dropdown-market', 'options'),
#     Input('market-dropdown-market', 'search_value')
# )
# def update_market_options_market(search_value):
#     query = "SELECT DISTINCT market FROM dim_market"
#     df = pd.read_sql(query, engine)
#     options = [{'label': m, 'value': m} for m in df['market']]
#     return options

# @callback(
#     Output('commodity-multi-dropdown-market', 'options'),
#     Input('commodity-multi-dropdown-market', 'search_value')
# )
# def update_commodity_multi_options_market(search_value):
#     query = "SELECT DISTINCT commodity FROM dim_commodity"
#     df = pd.read_sql(query, engine)
#     options = [{'label': c, 'value': c} for c in df['commodity']]
#     return options

# @callback(
#     Output('market-comparison-chart-market', 'figure'),
#     Input('market-dropdown-market', 'value'),
#     Input('commodity-multi-dropdown-market', 'value')
# )
# def update_market_comparison_chart_market(market, commodities):
#     if not market or not commodities:
#         return px.scatter()

#     commodities_str = "'" + "','".join(commodities) + "'"
#     query = f"""
#     SELECT c.commodity, f.wholesale, f.retail, d.date
#     FROM fact_market_prices f
#     JOIN dim_commodity c ON f.commodity_id = c.commodity_id
#     JOIN dim_market m ON f.market_id = m.market_id
#     JOIN dim_date d ON f.date_id = d.date_id
#     WHERE m.market = '{market}' AND c.commodity IN ({commodities_str})
#     ORDER BY d.date
#     """
#     df = pd.read_sql(query, engine)

#     fig = px.line(df, x='date', y=['wholesale', 'retail'], color='commodity',
#                   title=f"Price Comparison in {market} Market",
#                   labels={'value': 'Price', 'variable': 'Price Type'})

#     return fig