import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app

layout = dbc.Container([
        html.H3('Tables'),
        html.Br(),

    ],
    fluid=True,
    style={'padding': '20px'})
