import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app

# Markdown text
markdown_text_basic = '''
### DFT AND HRGASSORP Plotting

Version
0.3

Date:
04/16/2020

Authors: [Scott Angell](mailto:Scott.Angel@albemarle.com) and [Yupei Chen](mailto:Yupei.Chen@Albemarle.com)  
'''

markdown_text_todo = '''
#### ToDo: 

Tables

Customization
'''

markdown_text_done = '''
#### Done:

Multi-page

Navbar

Upload Page with Searchable Selector Table

Plotting
'''


layout = html.Div([
    dbc.Row([
        # Basic
        dbc.Col(dcc.Markdown(markdown_text_basic)),
        # Do List
        dbc.Col(dcc.Markdown(markdown_text_todo)),
        # Done
        dbc.Col(dcc.Markdown(markdown_text_done))
        ]),
    ],
    style={'padding': '20px'})

