import dash_bootstrap_components as dbc
from dash import dcc, html

# Style for the cards
CARD_STYLE = {
    "margin-bottom": "20px",
    "border": "1px solid #dee2e6",
    "border-radius": "5px",
}



map_page = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Kenyan Market Prices Map"),
            dcc.Dropdown(id='commodity-dropdown', placeholder='Select Commodity'),
            dcc.Dropdown(id='market-dropdown', placeholder='Select Market'),
            dcc.DatePickerRange(id='date-picker-range')
        ], width=4),
        dbc.Col([
            dcc.Graph(id='kenya-map')
        ], width=8)
    ])
])
