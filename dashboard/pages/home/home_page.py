import dash_bootstrap_components as dbc
from dash import dcc, html

# Style for the cards
CARD_STYLE = {
    "margin-bottom": "20px",
    "border": "1px solid #dee2e6",
    "border-radius": "5px",
}

home_page_content = dbc.Container(
    [
        html.H1("Project Homepage", className="text-center display-4 mt-4"),
        html.P(
            "Welcome to the homepage of our project. Here you can find information about the project,\
            access its GitHub repository, members, and contributors."
        ),
        html.Hr(),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H4("Project Description", className="card-title"),
                                            html.P(
                                                "Our project aims to provide valuable insights into Kenya's agricultural sector using data analytics techniques."
                                            ),
                                        ]
                                    )
                                ],
                                style=CARD_STYLE,
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H4("GitHub Repository", className="card-title"),
                                            html.P("Visit our GitHub repository to access the project code, documentation, and contribute to the project."),
                                            dbc.Button("GitHub Repository", color="primary", href="https://github.com/meaLuda/Kenya-Agric-Commodity-ETL", external_link=True),
                                        ]
                                    )
                                ],
                                style=CARD_STYLE,
                            ),
                            width=4,
                        ),
                    ]
                ),
            ],
        ),
        html.Hr(),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardImg(src="https://media.licdn.com/dms/image/D4D03AQHpZyjdVTitfQ/profile-displayphoto-shrink_400_400/0/1706949000782?e=1718841600&v=beta&t=LSeqRj84afdvqxTiksEs1FJ_txKQoJcidYO2yuWhwi8", top=True),
                                    dbc.CardBody(
                                        [
                                            html.H4("Munyala Eliud", className="card-title"),
                                            html.P(
                                                "Social Links:"
                                            ),
                                            html.A("LinkedIn: ", href="https://www.linkedin.com/in/eliud-munyala/", target="_blank", className="mr-1"),
                                            # breakline
                                            html.Br(),
                                            html.A("Twitter", href="https://www.twitter.com/member2", target="_blank", className="mr-1"),
                                        ]
                                    ),
                                ],
                                style=CARD_STYLE,
                            ),
                            width=4,
                        ),

                    ]
                ),
            ]
        ),
    ],
    fluid=True,
)
