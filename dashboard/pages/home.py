# import dash
# from dash import html, dcc
# import dash_bootstrap_components as dbc

# dash.register_page(__name__, path='/')

# layout = dbc.Container([
#     html.H1("Welcome to the Agricultural Market Dashboard", className="text-center mt-4"),
#     html.P("Explore commodity prices, market trends, and time series analysis using the navigation bar above.", className="text-center"),
#     dbc.Row([
#         dbc.Col(dbc.Card([
#             dbc.CardBody([
#                 html.H4("Commodity Analysis", className="card-title"),
#                 html.P("Analyze prices and trends for different commodities."),
#                 dbc.Button("Go to Commodity Analysis", href="/commodity", color="primary"),
#             ])
#         ]), width=4),
#         dbc.Col(dbc.Card([
#             dbc.CardBody([
#                 html.H4("Market Trends", className="card-title"),
#                 html.P("Explore market-wise trends and comparisons."),
#                 dbc.Button("Go to Market Trends", href="/market", color="primary"),
#             ])
#         ]), width=4),
#         dbc.Col(dbc.Card([
#             dbc.CardBody([
#                 html.H4("Time Series Analysis", className="card-title"),
#                 html.P("Analyze price trends over time for commodities."),
#                 dbc.Button("Go to Time Series", href="/timeseries", color="primary"),
#             ])
#         ]), width=4),
#     ], className="mt-4")
# ])