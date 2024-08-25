import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from app import engine

dash.register_page(__name__, path='/commodity')

layout = dbc.Container([
    html.H1("Commodity Analysis", className="text-center mt-4"),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='commodity-dropdown-commodity',
                options=[],
                value=None,
                placeholder="Select a commodity"
            )
        ], width=6),
        dbc.Col([
            dcc.Dropdown(
                id='price-type-dropdown-commodity',
                options=[
                    {'label': 'Wholesale Price', 'value': 'wholesale'},
                    {'label': 'Retail Price', 'value': 'retail'}
                ],
                value='wholesale',
                placeholder="Select price type"
            )
        ], width=6),
    ], className="mt-4"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='commodity-price-chart-commodity')
        ], width=12)
    ], className="mt-4"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='commodity-supply-chart-commodity')
        ], width=12)
    ], className="mt-4")
])

@callback(
    Output('commodity-dropdown-commodity', 'options'),
    Output('commodity-price-chart-commodity', 'figure'),
    Output('commodity-supply-chart-commodity', 'figure'),
    Input('commodity-dropdown-commodity', 'search_value'),
    Input('commodity-dropdown-commodity', 'value'),
    Input('price-type-dropdown-commodity', 'value'),
    prevent_initial_call=True
)
def update_commodity_data(search_value, commodity, price_type):
    # Update commodity dropdown options
    query = "SELECT DISTINCT commodity_name FROM dim_commodity"
    df_commodities = pd.read_sql(query, engine)
    options = [{'label': c, 'value': c} for c in df_commodities['commodity_name']]
    
    # Default empty figures
    empty_fig = px.scatter()

    if not commodity:
        return options, empty_fig, empty_fig

    # Query for charts
    query = f"""
    SELECT f.{price_type}, f.supply_volume, d.date
    FROM fact_market_prices f
    JOIN dim_commodity c ON f.commodity_id = c.commodity_id
    JOIN dim_date d ON f.date_id = d.date_id
    WHERE c.commodity_name = '{commodity}'
    ORDER BY d.date
    """
    df = pd.read_sql(query, engine)

    price_fig = px.scatter(df, x='date', y=price_type, title=f"{commodity} {price_type.capitalize()} Price Over Time")
    price_fig.update_traces(mode='lines+markers')

    supply_fig = px.scatter(df, x='date', y='supply_volume', title=f"{commodity} Supply Volume Over Time")
    supply_fig.update_traces(mode='lines+markers')

    return options, price_fig, supply_fig
