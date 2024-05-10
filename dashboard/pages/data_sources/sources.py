
from dash import dcc, html


# Data Sources Page Content
data_sources_content = html.Div(
    [
        html.H1("Data Sources", className="display-5"),
        html.P(
            "This page lists the various data sources used for Kenya's Agricultural insights, along with descriptions and links:"
        ),
        html.Br(),
        html.Div(
            [
                html.Strong("1. Ministry of Agriculture, Livestock, and Fisheries (MALF): "),
                html.P(
                    "KAMIS was developed to provide members and stakeholders with improved early warning marketing and trade information, leading to more efficient and competitive"
                ),
                dcc.Link("Access MALF Data", href="https://amis.co.ke/"),
            ],
            style={"margin-bottom": "1rem"},
        ),
    ],
    style={"padding": "2rem 1rem"},
)