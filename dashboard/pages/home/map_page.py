from dash import dcc, html, Input, Output, callback
import pandas as pd
from sqlalchemy import create_engine
import dash_bootstrap_components as dbc
import plotly.express as px

engine = create_engine('postgresql://postgres:RQaoNj7QEDxq@localhost:5433/Kemis_analytics_db')

# Load data
data = pd.read_sql_query("SELECT * FROM public.mv_market_summary_by_county_date_geo ORDER BY avg_retail_price DESC;", engine)
data_market = pd.read_sql_query("SELECT * FROM mv_market_summary_by_market_date_geo", engine)

layout = dbc.Container([
    html.H1("County Summary Map", className="text-center mb-5"),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Label("County Filter"),
                dcc.Dropdown(
                    id="county-filter",
                    options=[{"label": i, "value": i} for i in data["county"].unique()],
                    value=None,
                    multi=True,
                )
            ])
        ], md=4),
        dbc.Col([
            html.Div([
                html.Label("Date Range"),
                html.Br(),
                dcc.DatePickerRange(
                    id="date-range",
                    start_date=data["date"].min(),
                    end_date=data["date"].max(),
                )
            ])
        ], md=4),
        dbc.Col([
            html.Div([
                html.Label("Commodity Filter"),
                dcc.Dropdown(
                    id="commodity-filter",
                    options=[{"label": i, "value": i} for i in data["commodity"].unique()],
                    value=None,
                    multi=True,
                )
            ])
        ], md=4),
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="county-summary-map")
        ], md=12)
    ]),

    dbc.Row(html.Hr()),

    html.H1("Market Summary Map", className="text-center mb-5"),
    html.Hr(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Label("Market Filter"),
                dcc.Dropdown(
                    id="market-filter",
                    options=[{"label": i, "value": i} for i in data_market["market"].unique()],
                    value=None,
                    multi=True,
                )
            ])
        ], md=4),
        dbc.Col([
            html.Div([
                html.Label("Date Range"),
                html.Br(),
                dcc.DatePickerRange(
                    id="date-range-market",
                    start_date=data_market["date"].min(),
                    end_date=data_market["date"].max(),
                )
            ])
        ], md=4),
        dbc.Col([
            html.Div([
                html.Label("Market Commodity Filter"),
                dcc.Dropdown(
                    id="commodity-filter-market",
                    options=[{"label": i, "value": i} for i in data_market["commodity"].unique()],
                    value=None,
                    multi=True,
                )
            ])
        ], md=4),
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="market-summary-map")
        ], md=12)
    ]),

])

@callback(
    Output("county-summary-map", "figure"),
    [
        Input("county-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("commodity-filter", "value"),
    ],
)
def update_map(selected_counties, start_date, end_date, selected_commodities):
    filtered_data = data.copy()

    # Convert the 'date' column to datetime
    filtered_data["date"] = pd.to_datetime(filtered_data["date"])

    # Check if any filters are applied
    if selected_counties is None and selected_commodities is None:
        # No filters applied, show the entire dataset
        fig = px.scatter_mapbox(
            filtered_data,
            lat="latitude",
            lon="longitude",
            color="county",
            size_max=50,  # Adjust the maximum size of the data points
            hover_data=[
                "county",
                "commodity",
                "date",
                "avg_wholesale_price",
                "avg_retail_price",
                "total_supply_volume",
            ],
            zoom=5,
            height=600,
        )
    else:
        # Apply filters
        if selected_counties:
            filtered_data = filtered_data[filtered_data["county"].isin(selected_counties)]

        if start_date and end_date:
            filtered_data = filtered_data[
                (filtered_data["date"] >= start_date) & (filtered_data["date"] <= end_date)
            ]

        if selected_commodities:
            filtered_data = filtered_data[filtered_data["commodity"].isin(selected_commodities)]

        fig = px.scatter_mapbox(
            filtered_data,
            lat="latitude",
            lon="longitude",
            color="county",
            size="total_supply_volume",
            hover_data=[
                "county",
                "commodity",
                "date",
                "avg_wholesale_price",
                "avg_retail_price",
                "total_supply_volume",
            ],
            zoom=4,
            height=600,
        )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig



@callback(
    Output("market-summary-map", "figure"),
    [
        Input("market-filter", "value"),
        Input("date-range-market", "start_date"),
        Input("date-range-market", "end_date"),
        Input("commodity-filter-market", "value"),
    ],
)
def update_market_map(selected_markets, start_date, end_date, selected_commodities):
    filtered_data = data_market.copy()

    # Convert the 'date' column to datetime
    filtered_data["date"] = pd.to_datetime(filtered_data["date"])

    # Check if any filters are applied
    if selected_markets is None and selected_commodities is None:
        # No filters applied, show the entire dataset
        fig = px.scatter_mapbox(
            filtered_data,
            lat="latitude",
            lon="longitude",
            color="market",
            size_max=50,  # Adjust the maximum size of the data points
            hover_data=[
                "market",
                "commodity",
                "date",
                "avg_wholesale_price",
                "avg_retail_price",
                "total_supply_volume",
            ],
            zoom=5,
            height=600,
        )
    else:
        # Apply filters
        if selected_markets:
            filtered_data = filtered_data[filtered_data["market"].isin(selected_markets)]

        if start_date and end_date:
            filtered_data = filtered_data[
                (filtered_data["date"] >= start_date) & (filtered_data["date"] <= end_date)
            ]

        if selected_commodities:
            filtered_data = filtered_data[filtered_data["commodity"].isin(selected_commodities)]

        fig = px.scatter_mapbox(
            filtered_data,
            lat="latitude",
            lon="longitude",
            color="market",
            size="total_supply_volume",
            hover_data=[
                "market",
                "commodity",
                "date",
                "avg_wholesale_price",
                "avg_retail_price",
                "total_supply_volume",
            ],
            zoom=4,
            height=600,
        )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
