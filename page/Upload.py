import dash_core_components as dcc
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import re
import pandas as pd
import glob
import shutil
from datetime import datetime

from app import app

# region Constants

# DFT
col_DFT_p = ['Pore Diameter', 'Cum PV', 'Cum SA', 'dV/dlogD', 'dSA/dlogD']
col_DFT_f = ['P/P0', 'Fitted V', 'Measured V']

# HR
col_HR_p = ['Relative Pressure', 'Absolute Pressure', 'Adsorbed Amount', 'Elapsed Time', 'Saturation Pressure']
col_HR_a = ['BJH-A-CuPV_(Pore Width)', 'BJH-A-CuPV_(Pore Volume)', 'BJH-A-PoSD_(Pore Width)', 'BJH-A-PoSD_(dV/dlog(D)PV)']
col_HR_d = ['BJH-D-CuPV_(Pore Width)', 'BJH-D-CuPV_(Pore Volume)', 'BJH-D-PoSD_(Pore Width)', 'BJH-D-PoSD_(dV/dlog(D)PV)']

# Directories
directory = '//BYTALTX01/Reference/Other/Python/DFTnHR/Resources/Input/'
error_directory = '//BYTALTX01/Reference/Other/Python/DFTnHR/Resources/Input/Error/'

# endregion

# region Functions


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
        # TODO: Specify specific height eg. 300px
        style_table={'height': 'auto', 'overflowY': 'auto'},
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

# region Initialization

csvdict = pd.DataFrame()

csvlist = [f[len(directory):] for f in glob.glob(directory + '*.csv')]
sidlist = list(map(get_sid, csvlist))

csvdict.insert(0, 'FileName', csvlist)
csvdict.insert(1, 'SID', sidlist)

siddict = pd.DataFrame(data=set(sidlist), columns=['SID'])
siddict['id'] = siddict['SID']
siddict.set_index('id', inplace=True, drop=False)

# endregion

layout = html.Div([
        html.H3('Upload'),
        html.Br(),
        dbc.Card(
            [
                generate_sid_selector_table(siddict),
                html.Button(children='Generate Data', id='btn-generate', n_clicks=0),
                html.Div(children='', id='text-generate')
            ])
    ],
    style={'padding': '20px'})

# region Callbacks


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
