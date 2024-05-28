from dash import dcc, html, Input, Output, callback
import pandas as pd
from sqlalchemy import create_engine
import dash_bootstrap_components as dbc
import plotly.express as px

engine = create_engine('postgresql://postgres:RQaoNj7QEDxq@localhost:5433/Kemis_analytics_db')

# Load data
data = pd.read_sql_query("SELECT * FROM mv_market_summary_by_county_date", engine)


layout = dbc.Container([
    html.H1("Market Summary", className="text-center mb-5"),

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
        html.Br(),
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
        ], md=6),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="market-summary-graph")
        ], md=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2("Y-Axis Selection"),
                html.Br(),
                dcc.RadioItems(
                    id="y-axis-radio-items",
                    options=[
                        {"label": i, "value": i} for i in ["avg_wholesale_price", "avg_retail_price", "total_supply_volume"]
                    ],
                    value="avg_wholesale_price",
                    labelStyle={"display": "inline-block"},
                    className="mb-3",  # Add some margin below the radio items
                ),
            ])
        ], md=12)
    ]),
])

@callback(
    Output("market-summary-graph", "figure"),
    [
        Input("county-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("y-axis-radio-items", "value"),
    ],
)
def update_graph(selected_counties, start_date, end_date, y_axis_selection):
    if start_date is None and end_date is None:
        # Return the full data if no date range is selected
        fig = px.line(data, x="date", y=y_axis_selection, color="county", title="Market Summary")
        return fig

    # Convert the 'date' column to datetime
    data["date"] = pd.to_datetime(data["date"])

    filtered_data = data[
        (data["date"] >= start_date) & (data["date"] <= end_date)
    ]

    if selected_counties is None:
        # If no counties are selected, use the filtered data without county filtering
        fig = px.line(
            filtered_data, x="date", y=y_axis_selection, color="county", title="Market Summary"
        )
    else:
        # Filter the data by selected counties
        filtered_data = filtered_data[filtered_data["county"].isin(selected_counties)]
        fig = px.line(
            filtered_data, x="date", y=y_axis_selection, color="county", title="Market Summary"
        )

    return fig
