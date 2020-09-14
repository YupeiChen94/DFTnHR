import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
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
    html.Div(id='page-content'),

    # DF Storage
    dcc.Store(id='DFT-P', storage_type='memory'),
    dcc.Store(id='DFT-F', storage_type='memory'),
    dcc.Store(id='HR-P', storage_type='memory'),
    dcc.Store(id='HR-A', storage_type='memory'),
    dcc.Store(id='HR-D', storage_type='memory'),
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
        return Info.layout


if __name__ == '__main__':
    app.run_server()

    # Alternate Multi-page example
    # server.py
    # from flask import Flask
    #
    # server = Flask(__name__)
    #
    # app1.py
    # import dash
    # from server import server
    #
    # app = dash.Dash(name='app1', sharing=True, server=server, url_base_pathname='/app1')
    #
    # app2.py
    # import dash
    # from server import server
    #
    # app = dash.Dash(name='app2', sharing=True, server=server, url_base_pathname='/app2')
    #
    # run.py
    # from server import server
    # from app1 import app as app1
    # from app2 import app as app2
    #
    # if __name__ == '__main__':
    #     server.run()
