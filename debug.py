"""
Debug
Created on Fri Jan 3 09:23:07 2020
@author: chenyc2
"""

# region Imports
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import re
import glob
import shutil
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
directory = 'C:/Users/flute/PycharmProjects/DFTnHR/Resources/Input/'
error_directory = 'C:/Users/flute/PycharmProjects/DFTnHR/Resources/Error/'
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
    """Regex to return SID from filename"""
    return re.search("\\s[0-9]{7}\\s", filename).group()[1:8]


def read_csvs(sid_list):
    """Read csvs from directory with selected SIDs"""
    master_dft_p = pd.DataFrame()
    master_dft_f = pd.DataFrame()
    master_hr_p = pd.DataFrame()
    master_hr_a = pd.DataFrame()
    master_hr_d = pd.DataFrame()
    for index, row in csvdict[csvdict.SID.isin(sid_list)].iterrows():
        print(directory + row['FileName'])
        tempdf = pd.read_csv(directory + row['FileName'])
        csvtype = validate_csv(tempdf, row['FileName'])
        tempdf.insert(0, 'SID', row['SID'])
        if csvtype == 'DFT':
            master_dft_p = pd.concat([master_dft_p, tempdf[col_DFT_p + ['SID']].dropna()])
            master_dft_f = pd.concat([master_dft_f, tempdf[col_DFT_f + ['SID']].dropna()])
        elif csvtype == 'HR':
            master_hr_p = pd.concat([master_hr_p, tempdf[col_HR_p + ['SID']].dropna()])
            master_hr_a = pd.concat([master_hr_a, tempdf[col_HR_a + ['SID']].dropna()])
            master_hr_d = pd.concat([master_hr_d, tempdf[col_HR_d + ['SID']].dropna()])
        else:
            # TODO: Error message for user explaining that one of the files for the selected SIDs was not valid
            pass
    return master_dft_p.to_dict('records'), master_dft_f.to_dict('records'), master_hr_p.to_dict('records'), master_hr_a.to_dict('records'), master_hr_d.to_dict('records')


def validate_csv(dataframe, filename):
    """Pass in dataframe for validation by column headers, move file to error if no match"""
    tempcols = dataframe.columns
    if all(col in tempcols for col in col_DFT_f + col_DFT_p):
        return 'DFT'
    elif all(col in tempcols for col in col_HR_a + col_HR_p + col_HR_d):
        return 'HR'
    else:
        shutil.move(directory + filename, error_directory)
        return 'Error'


# endregion

# region Upload
# TODO: Truncate all values to 6 digits after decimal place

csvdict = pd.DataFrame()

csvlist = [f[len(directory):] for f in glob.glob(directory + '*.csv')]
sidlist = list(map(get_sid, csvlist))

csvdict.insert(0, 'FileName', csvlist)
csvdict.insert(1, 'SID', sidlist)

siddict = pd.DataFrame(data=set(sidlist), columns=['SID'])
siddict['id'] = siddict['SID']
siddict.set_index('id', inplace=True, drop=False)

# region Debug Initialization
df_DFT = pd.read_csv(directory + DFT_file)
df_HR = pd.read_csv(directory + HR_file)
DFT_sid = get_sid(DFT_file)
HR_sid = get_sid(HR_file)
df_DFT_pTable = df_DFT[col_DFT_p].dropna()
df_DFT_fTable = df_DFT[col_DFT_f].dropna()
df_HR_pTable = df_HR[col_HR_p].dropna()
df_HR_aTable = df_HR[col_HR_a].dropna()
df_HR_dTable = df_HR[col_HR_d].dropna()
df_DFT_pTable.insert(0, 'SID', DFT_sid)
df_DFT_fTable.insert(0, 'SID', DFT_sid)
df_HR_pTable.insert(0, 'SID', HR_sid)
df_HR_aTable.insert(0, 'SID', HR_sid)
df_HR_dTable.insert(0, 'SID', HR_sid)
df_DFT_pMaster = pd.concat([df_DFT_pMaster, df_DFT_pTable])
df_DFT_fMaster = pd.concat([df_DFT_fMaster, df_DFT_fTable])
df_HR_pMaster = pd.concat([df_HR_pMaster, df_HR_pTable])
df_HR_aMaster = pd.concat([df_HR_aMaster, df_HR_aTable])
df_HR_dMaster = pd.concat([df_HR_dMaster, df_HR_dTable])
# endregion

upload_page = dbc.Card(
    [
        dbc.CardHeader('Generate'),
        html.Br(),
        generate_sid_selector_table(siddict),
        html.Button(children='Generate', id='btn-generate', n_clicks=0),
        html.Div(children='', id='text-generate')
    ]
)

# endregion

# region Plots
# DFT_controls = dbc.Card(
#     [
#         dbc.CardHeader('DFT Axis'),
#         html.Br(),
#         dbc.FormGroup(
#             [
#                 dcc.Dropdown(
#                     id='dft-p-x-col',
#                     options=[{'label': i, 'value': i} for i in col_DFT_p],
#                     value='Pore Diameter'
#                 ),
#                 dcc.RadioItems(
#                     id='dft-p-x-type',
#                     options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
#                     value='Linear',
#                     labelStyle={'display': 'inline-block'})
#             ],
#             # style={'width': '48%', 'display': 'inline-block'}
#         ),
#         dbc.FormGroup(
#             [
#                 dcc.Dropdown(
#                     id='dft-p-y-col',
#                     options=[{'label': i, 'value': i} for i in col_DFT_p],
#                     value='Cum PV'
#                 ),
#                 dcc.RadioItems(
#                     id='dft-p-y-type',
#                     options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
#                     value='Linear',
#                     labelStyle={'display': 'inline-block'})
#             ],
#             # style={'width': '48%', 'display': 'inline-block'}
#         ),
#     ],
#     body=True,
#     # style={
#     #         'borderBottom': 'thin lightgrey solid',
#     #         'backgroundColor': 'rgb(250,250,250)',
#     #         'padding': '10px 5px'},
# )
# DFT_p_plot = dbc.Card(
#     [
#         dbc.CardHeader('DFT P Graph'),
#         dcc.Graph(
#             id='dft-p-graph'
#         )
#     ],
# )
# DFT_plot_card = dbc.Row(
#         [
#             dbc.Col(
#                 [
#                     DFT_controls,
#                 ]
#             ),
#             dbc.Col(
#                 [
#                     DFT_p_plot,
#                 ]
#             )
#         ]
#     )
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

# @app.callback(
#     Output('dft-p-graph', 'figure'),
#     [
#         Input('dft-p-x-col', 'value'),
#         Input('dft-p-y-col', 'value'),
#         Input('dft-p-x-type', 'value'),
#         Input('dft-p-y-type', 'value'),
#         Input('DFT-P', 'data')
#     ],
# )
# def make_dft_p_graph(x_col, y_col, x_type, y_type, table):
#     if table is None:
#         raise PreventUpdate
#     fig = px.line(table, x=x_col, y=y_col, color='SID')
#     fig.update_xaxes(title=x_col, type='linear' if x_type == 'Linear' else 'log')
#     fig.update_yaxes(title=y_col, type='linear' if y_type == 'Linear' else 'log')
#     return fig


@app.callback(
    [
        Output('text-generate', 'children'),
        Output('DFT-P', 'data'),
        Output('DFT-F', 'data'),
        Output('HR-P', 'data'),
        Output('HR-A', 'data'),
        Output('HR-D', 'data')
    ],
    [Input('btn-generate', 'n_clicks')],
    [State('sid-selector-table', 'derived_virtual_selected_row_ids')]
)
def update_upload_status(n_clicks, selected_row_ids):
    if n_clicks < 1:
        raise PreventUpdate
    else:
        if not selected_row_ids:
            raise PreventUpdate
            # TODO: Error message to user that no SIDS were selected
        else:
            master_dft_p, master_dft_f, master_hr_p, master_hr_a, master_hr_d = read_csvs(selected_row_ids)
            print(selected_row_ids)
            return 'Data generated for selected sample(s): {}'.format(selected_row_ids), master_dft_p, master_dft_f, master_hr_p, master_hr_a, master_hr_d
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
        # tables_page,
        # html.Br(),

        # Plots
        DFT_plot_card,
        html.Br(),

        # DF Storage
        dcc.Store(id='DFT-P', storage_type='memory'),
        dcc.Store(id='DFT-F', storage_type='memory'),
        dcc.Store(id='HR-P', storage_type='memory'),
        dcc.Store(id='HR-A', storage_type='memory'),
        dcc.Store(id='HR-D', storage_type='memory'),

        # Debug
        upload_page,
        html.Br(),
    ],
    fluid=True,
    style={'padding': '20px'}
)
# endregion

if __name__ == '__main__':
    app.run_server(debug=True)
