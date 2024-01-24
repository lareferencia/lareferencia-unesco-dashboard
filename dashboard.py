from dash import Dash, dcc, html, Input, Output, State, ctx
import dash_ag_grid as dag
import pandas as pd
import time
from data import get_all_data, get_categories_list, get_categories_list_from_data_frame, filter_data, filter_data_from_data_frame
import dash_bootstrap_components as dbc

# Obtener datos
data_frame = get_all_data()

codigo_a_pais = {
    'AR': 'Argentina',
    'BR': 'Brazil',
    'CR': 'Costa Rica',
    'EC': 'Ecuador',
    'ES': 'España',
    'UY': 'Uruguay',
    'PE': 'Peru',
    'MX': 'Mexico',
    'PA': 'Panama',
    'SV': 'El Salvador',
    ' CO': 'Colombia',
    ' CL': 'Chile'
}

# Modificar el nombre de la columna en el DataFrame
data_frame.rename(columns={'CODIGO': 'PAIS'}, inplace=True)

data_frame['PAIS'] = data_frame['PAIS'].map(codigo_a_pais)

excluded_columns = ['PAIS', 'Nombre de la iniciativa', 'WEB', 'CONTACTO']

time_inicial = time.time()

categories_dropdown = get_categories_list()

time_final = time.time()
time_ejecucion = time_final - time_inicial
print('Tiempo de ejecución de get_categories_list: ', time_ejecucion)

# dropdown options for subcategory
subcategory_options = []

# Define font awesome as an external stylesheet
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css',
    dbc.themes.BOOTSTRAP
]

# Agregar las hojas de estilo externas a la aplicación
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Ajustar el tipo de dato de la columna 'CONTACTO'
data_frame['CONTACTO'] = data_frame['CONTACTO'].astype(str)

# Agregar ícono a la columna de contacto si es diferente de NO INFO
#data_frame['CONTACTO'] = data_frame['CONTACTO'].apply(lambda x: f'<i class="fas fa-envelope" title="{x}"></i>' if x != 'NO INFO' else x)

# Ajustar el tipo de dato de la columna 'WEB'
data_frame['WEB'] = data_frame['WEB'].astype(str)

# Hipervínculo a la columna web si es diferente de NO INFO
#data_frame['WEB'] = data_frame['WEB'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>' if x != 'NO INFO' else x)

data_frame['Nombre de la iniciativa'] = data_frame['Nombre de la iniciativa'].astype(str)

# Columna adicional con el tooltip a la celda
data_frame['Nombre de la iniciativa_tooltip'] = data_frame.apply(
    lambda row: f'{row["Nombre de la iniciativa"]}: {row["Función de la iniciativa"]}',
    axis=1
)

""" data_frame['Nombre de la iniciativa'] = data_frame.apply(
    lambda row: f'<i class="fas fa-info-circle"></i> {row["Nombre de la iniciativa"]}',
    axis=1
) """

app.layout = html.Div([
    html.H1(children='Dashboard recomendaciones UNESCO', style={'textAlign': 'center'}),
    html.Div([
        dcc.Dropdown(
            id='column-dropdown',
            options=categories_dropdown,
            placeholder='Seleccione una o varias categorías o subcategorías... ',
            multi=True,
            style={'width': '100%'}
        ),
        dcc.Dropdown(
            id='countries-dropdown',
            options=[{'label': pais, 'value': pais} for pais in data_frame['PAIS'].unique()],
            multi=True,
            placeholder='Seleccione uno o varios países...',
            style={'background-color': '#cefad0', 'width': '100%'}
        )],
        style={'textAlign': 'center', 'background-color': 'lightgrey', 'display': 'flex',
               'justify-content': 'center', 'flex-direction': 'column'}),

        html.Div(
        style={'display':'flex','width':'100%'},
        children=[
            html.Div(
                style={'width':'100%'},
                children=[
                    dag.AgGrid(
                        id='data-table',
                        columnDefs=[
                            {'headerName': 'PAIS' if col == 'CODIGO' else col, 'field': col,
                             'filter': True,
                             'sortable': True if col == 'PAIS' else False,
                             'cellRenderer': "ContactoButton" if col == 'CONTACTO' else
                             "WebButton" if col == 'WEB' else
                             "IniciativaComponent" if col == 'Nombre de la iniciativa' else None,
                             'maxWidth': 100 if col == 'PAIS' else
                             150 if col == 'WEB' else None,
                             'minWidth': 350 if col == 'Nombre de la iniciativa' else None,
                             }
                            for col in excluded_columns
                        ],
                        rowData=data_frame[excluded_columns].to_dict('records'),
                        className="ag-theme-balham",
                        columnSize="responsiveSizeToFit",
                        dashGridOptions={
                            'pagination': True,
                            'paginationAutoPageSize': True,
                            'rowSelection': 'single',
                        },
                        defaultColDef={
                            'resizable': True,
                        },
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
            ),            

        ],
    ),
], style={'padding': '20px'})

@app.callback(
    [
        Output('data-table', 'rowData'),
        Output('column-dropdown', 'options'),
        Output('countries-dropdown', 'options')
    ],
    [Input('column-dropdown', 'value'),
     Input('countries-dropdown', 'value')]
)
def update_table(selected_category, selected_countries):
    # caso en el que no haya filtrado
    if not selected_category and not selected_countries:
        print('No hay filtros')
        # Si no se ha seleccionado ninguna columna o se selecciona Todas, muestra todas las filas
        return data_frame[excluded_columns].to_dict('records'), categories_dropdown, data_frame['PAIS'].unique()

    # caso en el que haya filtrado por paises pero no por categorias
    if not selected_category and selected_countries:
        print('Filtrado por paises')
        filtered_df = data_frame[data_frame['PAIS'].isin(selected_countries)]
        # nuevas categorias y subcategorias a partir de los datos filtrados
        new_categories_dropdown = get_categories_list_from_data_frame(filtered_df)
        return filtered_df[excluded_columns].to_dict('records'), new_categories_dropdown, filtered_df['PAIS'].unique()

    # caso en el que haya filtrado por categorias pero no por paises
    if selected_category and not selected_countries:
        print('Filtrado por categorias')
        filtered_df = filter_data(selected_category)
        # nuevas categorias y subcategorias a partir de los datos filtrados
        new_categories_dropdown = get_categories_list_from_data_frame(filtered_df)
        return filtered_df[excluded_columns].to_dict('records'), new_categories_dropdown, filtered_df['PAIS'].unique()

    # caso en el que haya filtrado por categorias y paises
    print('Filtrado por categorias y paises')
    time_inicial = time.time()
    # pasar el filtro de pais antes de filtrar por categorias
    filtered_df = data_frame[data_frame['PAIS'].isin(selected_countries)]

    # pasar el filtro de categorias despues de filtrar por paises
    filtered_df = filter_data_from_data_frame(selected_category, filtered_df)

    # nuevas categorias y subcategorias a partir de los datos filtrados
    new_categories_dropdown = get_categories_list_from_data_frame(filtered_df)

    time_final = time.time()
    time_ejecucion = time_final - time_inicial
    print('Tiempo de ejecución de callback: ', time_ejecucion)

    return filtered_df[excluded_columns].to_dict('records'), new_categories_dropdown, filtered_df['PAIS'].unique()

#callback para el modal
@app.callback(
    [
        Output('modal', 'is_open'),
        Output('modal-body', 'children')
    ],
    [
        Input('data-table', 'cellClicked'),
        Input("row-selection-modal-close", "n_clicks"),
    ],
)
def update_card_info(selected_cell, is_open):
    if ctx.triggered_id == "row-selection-modal-close":
        return False, None
    if  selected_cell and not is_open:
        row_index = selected_cell['rowIndex']
        col_id = selected_cell['colId']
        cell_value = data_frame.iloc[row_index][col_id]
        # Check if cell_value is present in 'Nombre de la iniciativa' column
        if cell_value in data_frame['Nombre de la iniciativa'].values:
            function_of_initiative = data_frame.loc[data_frame['Nombre de la iniciativa'] == cell_value, 'Función de la iniciativa'].values[0]

            card_content = [
                html.H4(str(cell_value), style={'color': 'white', 'background-color': '#007BFF', 'padding': '10px'}),
                html.P(function_of_initiative, style={'margin': '10px'}),
            ]
            return True, card_content
        else:
            return False, []
    return False, []



if __name__ == '__main__':
    app.run_server(debug=True)
