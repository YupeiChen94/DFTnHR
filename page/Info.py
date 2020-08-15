import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app

# Markdown text
markdown_text_basic = '''
### DFT AND HRGASSORP Plotting

Version
0.1

Date:
04/16/2020

Authors: [Scott Angell](mailto:Scott.Angel@albemarle.com) and [Yupei Chen](mailto:Yupei.Chen@Albemarle.com)  
'''

markdown_text_todo = '''
#### ToDo:

Upload page will have text field to enter SID  

Will then search directory for each SID  

Needs to notify user if SID does not exist  

Visual Feedback on files read in to user  

File Upload

Plotting

Tables

Callbacks

Customization
'''

markdown_text_done = '''
#### Done:

Multi-page

Navbar
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

