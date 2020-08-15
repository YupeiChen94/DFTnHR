"""
Debug

Created on Fri Jan  3 09:23:07 2020

@author: chenyc2
"""

# region Imports
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import re
import glob
from datetime import datetime
# endregion

# region Constants
external_stylesheets = dbc.themes.BOOTSTRAP

app = dash.Dash(__name__, external_stylesheets=[external_stylesheets])

# DFT constants
df_DFT_pMaster = pd.DataFrame()
df_DFT_fMaster = pd.DataFrame()
col_DFT_p = ['Pore Diameter', 'Cum PV', 'Cum SA', 'dV/dlogD', 'dSA/dlogD']
col_DFT_f = ['P/P0', 'Fitted V', 'Measured V']

# HR constants
df_HR_pMaster = pd.DataFrame()
df_HR_aMaster = pd.DataFrame()
df_HR_dMaster = pd.DataFrame()
col_HR_p = ['Relative Pressure', 'Absolute Pressure', 'Adsorbed Amount', 'Elapsed Time', 'Saturation Pressure']
col_HR_a = ['BJH-A-CuPV_(Pore Width)', 'BJH-A-CuPV_(Pore Volume)', 'BJH-A-PoSD_(Pore Width)', 'BJH-A-PoSD_(dV/dlog(D)PV)']
col_HR_d = ['BJH-D-CuPV_(Pore Width)', 'BJH-D-CuPV_(Pore Volume)', 'BJH-D-PoSD_(Pore Width)', 'BJH-D-PoSD_(dV/dlog(D)PV)']

# Debugging Constants
directory = 'C:/Users/flute/PycharmProjects/Albemarle/DFTnHR/Resources/Input/'
DFT_file = 'HRSA2420 6717330 DFT_POSD 6619007_report_01-201909252150953_Table.csv'
HR_file = 'HRSA2420 6717330 HR_GASSORP 000-617_Table.csv'
# endregion


# region Functions
def generate_dash_table(df):
    """Data Table with only scrollbar"""
    dt = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        style_cell={'textAlign': 'left'},
        page_action='none',
        fixed_rows={'headers': True},
        style_table={'height': '300px', 'overflowY': 'auto'},
        css=[{'selector': '.row', 'rule': 'margin: 0'}]
    )
    return dt


def generate_sid_selector_table(df):
    """Data Table with scrollbar, filtering, and selector"""
    dt = dash_table.DataTable(
        id='sid-selector-table',
        data=df.to_dict('records'),
        columns=[{'id': str(c), 'name': str(c)} for c in df.columns if c != 'id'],
        filter_action="native",
        sort_action="native",
        row_selectable="multi",
        selected_rows=[],
        style_cell={'textAlign': 'right'},
        page_action='none',
        fixed_rows={'headers': True},
        style_table={'height': '300px', 'overflowY': 'auto'},
        css=[{'selector': '.row', 'rule': 'margin: 0'}]
    )
    return dt


def get_sid(filename):
    return re.search("\\s[0-9]{7}\\s", filename).group()[1:8]
# endregion


# region Upload
csvdict = pd.DataFrame()

csvlist = [f[len(directory):] for f in glob.glob(directory + '*.csv')]
sidlist = list(map(get_sid, csvlist))

csvdict.insert(0, 'FileName', csvlist)
csvdict.insert(1, 'SID', sidlist)

siddict = pd.DataFrame(data=set(sidlist), columns=['SID'])
siddict['id'] = siddict['SID']
siddict.set_index('id', inplace=True, drop=False)

# TODO: Allow user selection of SIDS to grab using a datatable

# Read in csv's
df_DFT = pd.read_csv(directory + DFT_file)
df_HR = pd.read_csv(directory + HR_file)

# Regex SID from filename
DFT_sid = get_sid(DFT_file)
HR_sid = get_sid(HR_file)

# TODO: Integrity check of uploaded files
# TODO: Truncate all values to 6 digits after decimal place

# Column selection and dropping blank rows
df_DFT_pTable = df_DFT[col_DFT_p].dropna()
df_DFT_fTable = df_DFT[col_DFT_f].dropna()

df_HR_pTable = df_HR[col_HR_p].dropna()
df_HR_aTable = df_HR[col_HR_a].dropna()
df_HR_dTable = df_HR[col_HR_d].dropna()

# Append SID to each row
df_DFT_pTable.insert(0, 'SID', DFT_sid)
df_DFT_fTable.insert(0, 'SID', DFT_sid)

df_HR_pTable.insert(0, 'SID', HR_sid)
df_HR_aTable.insert(0, 'SID', HR_sid)
df_HR_dTable.insert(0, 'SID', HR_sid)

# Append temp table to master table for each file uploaded
df_DFT_pMaster = pd.concat([df_DFT_pMaster, df_DFT_pTable])
df_DFT_fMaster = pd.concat([df_DFT_fMaster, df_DFT_fTable])

df_HR_pMaster = pd.concat([df_HR_pMaster, df_HR_pTable])
df_HR_aMaster = pd.concat([df_HR_aMaster, df_HR_aTable])
df_HR_dMaster = pd.concat([df_HR_dMaster, df_HR_dTable])

upload_page = dbc.Card(
    [
        dbc.CardHeader('Generate'),
        html.Br(),
        html.Button(children='Generate', id='btn-generate', n_clicks=0),
        html.Div(children='', id='text-generate')
    ]
)

# endregion

# region Plots
# TODO: Create DFT Plots
# TODO: Restriction that x and y cannot be same column
DFT_controls = dbc.Card(
    [
        dbc.CardHeader('DFT Axis'),
        html.Br(),
        dbc.FormGroup(
            [
                dcc.Dropdown(
                    id='dft-p-x-col',
                    options=[{'label': i, 'value': i} for i in col_DFT_p],
                    value='Pore Diameter'
                ),
                dcc.RadioItems(
                    id='dft-p-x-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'})
            ],
            # style={'width': '48%', 'display': 'inline-block'}
        ),
        dbc.FormGroup(
            [
                dcc.Dropdown(
                    id='dft-p-y-col',
                    options=[{'label': i, 'value': i} for i in col_DFT_p],
                    value='Pore Diameter'
                ),
                dcc.RadioItems(
                    id='dft-p-y-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'})
            ],
            # style={'width': '48%', 'display': 'inline-block'}
        ),
    ],
    body=True,
    # style={
    #         'borderBottom': 'thin lightgrey solid',
    #         'backgroundColor': 'rgb(250,250,250)',
    #         'padding': '10px 5px'},
)
DFT_p_plot = dbc.Card(
    [
        dbc.CardHeader('DFT P Graph'),
        dcc.Graph(
            id='dft-p-graph'
        )
    ],
)
DFT_plot_card = dbc.Row(
        [
            dbc.Col(
                [
                    DFT_controls,
                ]
            ),
            dbc.Col(
                [
                    DFT_p_plot,
                ]
            )
        ]
    )
# TODO: Create HR Plots
# endregion

# region Tables
tables_page = dbc.Row([
        # DFT Column
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader('DFT'),
                    html.Br(),
                    dbc.FormGroup([
                        dbc.Label('Pressure'),
                        generate_dash_table(df_DFT_pMaster),
                    ]),
                    dbc.FormGroup([
                        dbc.Label('Fitted'),
                        generate_dash_table(df_DFT_fMaster),
                    ]),
                ],
                body=True,
            ),
        ),
        # HR Column
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader('HR'),
                    html.Br(),
                    dbc.FormGroup([
                        dbc.Label('Pressure'),
                        generate_dash_table(df_HR_pMaster),
                    ]),
                    dbc.FormGroup([
                        dbc.Label('Adsorption'),
                        generate_dash_table(df_HR_aMaster),
                    ]),
                    dbc.FormGroup([
                        dbc.Label('Desorption'),
                        generate_dash_table(df_HR_dMaster),
                    ]),
                ],
                body=True,
            )
        )
    ])
# endregion


# region Callbacks
# TODO: Create reactive elements
# region DFT P graph
@app.callback(
    Output('dft-p-graph', 'figure'),
    [
        Input('dft-p-x-col', 'value'),
        Input('dft-p-y-col', 'value'),
        Input('dft-p-x-type', 'value'),
        Input('dft-p-y-type', 'value'),
    ],
)
def make_dft_p_graph(x_col, y_col, x_type, y_type):
    fig = px.line(df_DFT_pMaster, x=x_col, y=y_col, color='SID')
    fig.update_xaxes(title=x_col, type='linear' if x_type == 'Linear' else 'log')
    fig.update_yaxes(title=y_col, type='linear' if y_type == 'Linear' else 'log')
    return fig
# endregion

# region Generate Button
@app.callback(
    Output('text-generate', 'children'),
    [
        Input('btn-generate', 'n_clicks')
        # Input('selected-sid', 'value')
    ]
)
def update_upload_status(n_clicks):
    if n_clicks < 1:
        return ''
    return 'Data generated for selected samples!'
# endregion


# region Debug Selected from SID Table
@app.callback(
    Output('text-selected', 'children'),
    [
        Input('sid-selector-table', 'derived_virtual_row_ids'),
        Input('sid-selector-table', 'selected_row_ids')
    ]
)
def update_text_selected(row_ids, selected_row_ids):
    selected_id_set = set(selected_row_ids or [])

    if row_ids is None:
        return 'NO ROW_IDS'
        # siddict2 = siddict
        # row_ids = siddict['id']
    else:
        # return selected_row_ids
        # return siddict.to_string()
        # return siddict.loc[row_ids]
        pass

    return '"{}"'.format(selected_row_ids)

# endregion

# endregion

# region Customization
# TODO: Add customization options
# TODO: Use keys and a separate table for user customization instead of modifying master table directly
# endregion


# region Design
app.layout = dbc.Container(
    [
        # Title
        html.H1('DEBUG'),
        html.Hr(),
        html.H6('Time is {}'.format(datetime.now())),
        html.Br(),

        # Table
        tables_page,
        html.Br(),

        # Plots
        DFT_plot_card,
        html.Br(),

        # Debug
        generate_sid_selector_table(siddict),
        upload_page,
        html.Br(),
        html.Div(children='', id='text-selected')
    ],
    fluid=True,
    style={'padding': '20px'}
)
# endregion

if __name__ == '__main__':
    app.run_server(debug=True)
