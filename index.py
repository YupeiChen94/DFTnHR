import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app
from page import Info, Upload, Options, Graphs, Tables

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Information", href="/page/Information")),
        dbc.NavItem(dbc.NavLink("Upload", href="/page/Upload")),
        dbc.NavItem(dbc.NavLink("Options", href="/page/Options")),
        dbc.NavItem(dbc.NavLink("Graphs", href="/page/Graphs")),
        dbc.NavItem(dbc.NavLink("Tables", href="/page/Tables")),
    ],
    brand="SA Plotting Tool",
    brand_href="#",
    fluid=True,
    sticky='top',
    color='primary',
    dark=True,
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page/Information':
        return Info.layout
    elif pathname == '/page/Upload':
        return Upload.layout
    elif pathname == '/page/Options':
        return Options.layout
    elif pathname == '/page/Graphs':
        return Graphs.layout
    elif pathname == '/page/Tables':
        return Tables.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
