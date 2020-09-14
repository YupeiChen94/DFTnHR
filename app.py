import flask
import dash
import dash_bootstrap_components as dbc

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB], suppress_callback_exceptions=True)
# server = app.server
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.SPACELAB], suppress_callback_exceptions=True)
