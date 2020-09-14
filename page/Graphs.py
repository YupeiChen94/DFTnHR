import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px

from app import app

# region Constants
col_DFT_p = ['Pore Diameter', 'Cum PV', 'Cum SA', 'dV/dlogD', 'dSA/dlogD']
col_DFT_f = ['P/P0', 'Fitted V', 'Measured V']
col_HR_p = ['Relative Pressure', 'Absolute Pressure', 'Adsorbed Amount', 'Elapsed Time', 'Saturation Pressure']
col_HR_a = ['BJH-A-CuPV_(Pore Width)', 'BJH-A-CuPV_(Pore Volume)', 'BJH-A-PoSD_(Pore Width)', 'BJH-A-PoSD_(dV/dlog(D)PV)']
col_HR_d = ['BJH-D-CuPV_(Pore Width)', 'BJH-D-CuPV_(Pore Volume)', 'BJH-D-PoSD_(Pore Width)', 'BJH-D-PoSD_(dV/dlog(D)PV)']
# endregion

# region Styling
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}
dft_colors = {
    'background': ''
}
# endregion


# region Functions
def get_column_list(tab):
    if tab == 'DFT-P-tab':
        return col_DFT_p
    elif tab == 'DFT-F-tab':
        return col_DFT_f
    elif tab == 'HR-P-tab':
        return col_HR_p
    elif tab == 'HR-A-tab':
        return col_HR_a
    elif tab == 'HR-D-tab':
        return col_HR_d
# endregion


# region Objects
def create_controls(col_list):
    plot_controls = dbc.Card(
        [
            dbc.FormGroup(
                [
                    dbc.Label('X-Axis'),
                    dcc.Dropdown(
                        id='x-col',
                        options=[{'label': i, 'value': i} for i in col_list],
                        value=col_list[0]
                    ),
                    dcc.RadioItems(
                        id='x-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'margin-right': '10px'}
                    )
                ],
            ),
            dbc.FormGroup(
                [
                    dbc.Label('Y-Axis'),
                    dcc.Dropdown(
                        id='y-col',
                        options=[{'label': i, 'value': i} for i in col_list],
                        value=col_list[1]
                    ),
                    dcc.RadioItems(
                        id='y-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'margin-right': '10px'}
                    )
                ],
            ),
        ],
        body=True,
        style={
                'borderBottom': 'thin lightgrey solid',
                'backgroundColor': 'rgb(250,250,250)',
                'padding': '10px 10px'},
    )
    return plot_controls


def create_plot():
    graph_plot = dbc.Card(
        [
            # dbc.CardHeader('Plot Header'),
            dcc.Graph(
                id='graph'
            )
        ]
    )
    return graph_plot
# endregion


layout = html.Div([
        html.H3('Graphs'),
        html.Br(),
        dcc.Tabs(id='tabs', value='DFT-P-tab', children=[
            dcc.Tab(label='DFT Pressure', value='DFT-P-tab', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='DFT Fitted', value='DFT-F-tab', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='HR Pressure', value='HR-P-tab', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='HR Adsorption', value='HR-A-tab', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='HR Desorption', value='HR-D-tab', style=tab_style, selected_style=tab_selected_style),
        ], vertical=True, parent_style={'float': 'left'}),
        dbc.Container([
            html.Div(id='graph-content')
        ], fluid=True)
    ],
    style={'padding': '20px'})


@app.callback(
    Output('graph-content', 'children'),
    [Input('tabs', 'value')]
)
def render_graph_content(tab):
    if tab is None:
        raise PreventUpdate
    controls = create_controls(get_column_list(tab))
    plot = create_plot()
    return html.Div([
        dbc.Row(
            [
                dbc.Col(controls, width=3),
                dbc.Col(plot, width=9)
            ],
        )
    ])


@app.callback(
    Output('graph', 'figure'),
    [
        Input('x-col', 'value'),
        Input('y-col', 'value'),
        Input('x-type', 'value'),
        Input('y-type', 'value'),
        Input('tabs', 'value')
    ],
    [
        State('DFT-P', 'data'),
        State('DFT-F', 'data'),
        State('HR-P', 'data'),
        State('HR-A', 'data'),
        State('HR-D', 'data')
    ]
)
def create_graph(x_col, y_col, x_type, y_type, tab, dftp, dftf, hrp, hra, hrd):
    if tab == 'DFT-P-tab':
        table = dftp
    elif tab == 'DFT-F-tab':
        table = dftf
    elif tab == 'HR-P-tab':
        table = hrp
    elif tab == 'HR-A-tab':
        table = hra
    elif tab == 'HR-D-tab':
        table = hrd
    else:
        raise PreventUpdate
    if table is None:
        raise PreventUpdate
    fig = px.line(table, x=x_col, y=y_col, color='SID')
    fig.update_xaxes(title=x_col, type='linear' if x_type == 'Linear' else 'log')
    fig.update_yaxes(title=y_col, type='linear' if y_type == 'Linear' else 'log')
    return fig


@app.callback(
    Output('x-col', 'options'),
    [Input('y-col', 'value')],
    [State('tabs', 'value')],
        )
def filter_options(v, tab):
    return [{'label': i, 'value': i, 'disabled': i == v} for i in get_column_list(tab)]


@app.callback(
    Output('y-col', 'options'),
    [Input('x-col', 'value')],
    [State('tabs', 'value')]
)
def filter_options(v, tab):
    return [{'label': i, 'value': i, 'disabled': i == v} for i in get_column_list(tab)]
