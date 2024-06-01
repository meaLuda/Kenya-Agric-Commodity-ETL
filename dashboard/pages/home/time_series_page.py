from dash import dcc, html,callback
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from ..data.load import load_data
# Read the data

df = load_data("SELECT * FROM mv_price_time_series LIMIT 5000;")

df['date'] = pd.to_datetime(df['date'])



TIME_SERIES_PAGE = html.Div([
    html.H1("Commodity Prices Time Series"),

    html.Div([
        html.Label('Select Date Range:'),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=df['date'].min(),
            end_date=df['date'].max(),
            display_format='Y-MM-DD'
        )
    ]),

    html.Div([
        html.Label('Select Commodity:'),
        dcc.Dropdown(
            id='commodity-dropdown',
            options=[{'label': com, 'value': com} for com in df['commodity'].unique()],
            value=df['commodity'].unique()[0]
        )
    ]),

    html.Div([
        html.Label('Select Market:'),
        dcc.Dropdown(
            id='market-dropdown',
            options=[{'label': market, 'value': market} for market in df['market'].unique()],
            value=df['market'].unique()[0]
        )
    ]),

    dcc.Graph(id='price-time-series')
])

@callback(
    Output('price-time-series', 'figure'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('commodity-dropdown', 'value'),
        Input('market-dropdown', 'value')
    ]
)
def update_graph(start_date, end_date, selected_commodity, selected_market):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date) &
                     (df['commodity'] == selected_commodity) & (df['market'] == selected_market)]

    if filtered_df.empty:
        return {
            'data': [],
            'layout': {
                'title': 'No data available for the selected criteria'
            }
        }

    # Aggregate the data by averaging prices for each date, selecting only numeric columns
    aggregated_df = filtered_df.groupby('date')[['wholesale_price', 'retail_price']].mean().reset_index()

    fig = px.line(aggregated_df, x='date', y=['wholesale_price', 'retail_price'],
                  labels={'value': 'Price', 'variable': 'Price Type'},
                  title=f'Wholesale and Retail Prices Over Time for {selected_commodity} in {selected_market}')

    return fig
