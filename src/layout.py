from dash import html,dcc
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

# uo one level up to import the translate function
from translate.translate import translate

#Seleccionar columnas a mostrar en el grid
excluded_columns = ['PAIS', 'Nombre de la iniciativa','Detalles', 'WEB', 'CONTACTO']

#set language
lang = 'en'

#get language
def get_language():
    return lang
#set language
def set_language(l):
    global lang
    lang = l
    print('Language set to ', lang)

def getLayout(categories_dropdown,data_frame,unesco_options):
    layout = html.Div(
        id='layout',
        children=[
        html.Meta(charSet='utf-8'),
        html.Div(
                style={'width':'30%'},
                children=[
                            dcc.Dropdown(
                                id='language-dropdown',
                                options=[{'label': 'English', 'value': 'en'},{'label': 'Español', 'value': 'es'}],
                                placeholder=translate(lang,'Select_a_language'),
                                value=lang,
                                multi=False,)]),
        html.Div([
        html.Div([    
            dcc.Dropdown(
                id='countries-dropdown',
                options=[{'label': pais, 'value': pais} for pais in data_frame['PAIS'].unique()],
                multi=True,
                placeholder=translate(lang,u'Select_a_country'),
                style={'width': '100%'}
            ),
        ], style={'width': '30%'}),
        html.Div([
            dcc.Dropdown(
                id='column-dropdown',
                options=categories_dropdown,
                placeholder=translate(lang,'Select_a_category'),
                multi=True,
                style={'width': '100%'}
            ),
        ], style={'flex': '1'}),

            ],
            style={ 'background-color': '#CFD8DC', 'display': 'flex'}),
            html.Div(
                style={'width':'100%'},
                children=[
                            dcc.Dropdown(
                                id='objetivos-dropdown',
                                options=unesco_options,
                                placeholder=translate(lang,'Select_an_UNESCO_objective'),
                                multi=True,)]),
            html.Div(
            style={'display':'flex'},
            children=[

                dag.AgGrid(
                    id='data-table',
                    columnDefs=[
                        {'headerName': 'País' if col == 'PAIS' else 
                                        'Web' if col == 'WEB' else 
                                        'Contacto' if col == 'CONTACTO' else col,
                            'field': col,
                            'filter': True if col in ['PAIS','Nombre de la iniciativa'] else None,
                            'sortable': True if col == 'PAIS' else False,
                            'cellRenderer': "ContactoButton" if col == 'CONTACTO' else
                            "WebButton" if col == 'WEB' else
                            "IniciativaComponent" if col == 'Nombre de la iniciativa' else 
                            "DetallesComponent" if col == 'Detalles' else None,
                            'maxWidth': 120 if col =='Detalles' else 
                                        100 if col == 'WEB' else None,
                            'minWidth': 750 if col == 'Nombre de la iniciativa' else 
                                        125 if col == 'PAIS' else 
                                        120 if col == 'Detalles' else None,
                            }
                        for col in excluded_columns
                    ],
                    rowData=data_frame[excluded_columns].to_dict('records'),
                    className="ag-theme-material",
                    columnSize='responsiveSizeToFit',
                    dashGridOptions={
                        'pagination': True,
                        'paginationAutoPageSize': True,
                        "icons": {
                            'menu': '<i class="fa fa-search" aria-hidden="true"></i>',
                        }
                    },
                    defaultColDef={
                        'resizable': True,
                    },
                    getRowStyle = {
                    "styleConditions": [
                        {
                        "condition": "params.rowIndex % 2 === 0",
                        "style": {"backgroundColor": "#CFD8DC"},
                    },
                ]
                },
                style={'height': '800px'}
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(id='modal-header'),
                        dbc.ModalBody(id='modal-body'),
                        dbc.ModalFooter(dbc.Button("Close", id="row-selection-modal-close", className="ml-auto"),style={'display':'none'}),
                    ],
                    id='modal',
                    size='lg',
                    centered=True,
                    is_open=False,
                ),
            ],
        className='header1'
        ),
    ], style={'padding': '20px'})
    return layout

