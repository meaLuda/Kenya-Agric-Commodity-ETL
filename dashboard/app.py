import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

from pages.data_sources import sources
from pages.home import home_page

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow": "auto",
    "transition": "margin-left 0.5s",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "22rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H4("Kenya Agriculture Insights", className="display-4 ml-3 mt-4 mb-4"),
        html.Hr(),
        html.P(
            "An extensive analytics dashboard using "
            "data from different sources on Kenya's Agricultural Sector",
            className="lead",
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Data Sources", href="/d_sources", active="exact"),
                dbc.NavLink("Summary Report", href="/Summary Analytics", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

# Toggle button to show/hide sidebar
toggle_button = html.Button(
    html.Span(className="navbar-toggler-icon"),
    className="navbar-toggler",
    style={"position": "absolute", "left": "1rem", "top": "1rem"},
    id="toggle-button",
)

app.layout = html.Div([toggle_button, dcc.Location(id="url"), sidebar, content])


# Callback to toggle sidebar
@app.callback(
    Output("sidebar", "style"),
    [Input("toggle-button", "n_clicks")],
    prevent_initial_call=True,
)
def toggle_sidebar(n):
    if n and n % 2 == 1:
        return {"margin-left": "-20rem"}
    else:
        return SIDEBAR_STYLE


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home_page.home_page_content
    elif pathname == "/d_sources":
        return sources.data_sources_content
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=3000)
