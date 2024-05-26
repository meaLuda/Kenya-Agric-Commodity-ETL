import dash_bootstrap_components as dbc
from dash import dcc, html

# Style for the cards
CARD_STYLE = {
    "margin-bottom": "20px",
    "border": "1px solid #dee2e6",
    "border-radius": "5px",
}

map_view = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Kenyan Market Prices Time Series", className="text-center"), width=12),
        dbc.Col(html.Div(className="my-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id="commodity-dropdown", placeholder="Select Commodity", style={"width": "100%"}),
        ], width=3, className="mb-2"),
        dbc.Col([
            dcc.Dropdown(id="market-dropdown", placeholder="Select Market", style={"width": "100%"}),
        ], width=3, className="mb-2"),
        dbc.Col([
            dcc.DatePickerRange(id="date-picker-range", style={"width": "100%"}),
        ], width=6, className="mb-2"),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="kenya-timeseries")
        ], width=12)
    ])
], fluid=True)
