from dash import Dash, dcc, html, Input, Output, dash_table

import pandas as pd

from data import *

data_frame = get_all_data()

codigo_a_pais = {
    'AR': 'Argentina',
    'BR': 'Brazil',
    'CR': 'Costa Rica',
    'EC': 'Ecuador',
    'ES': 'Espana',
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

rest_columns = data_frame.columns[5:]

time_inicial = time.time()

categories_dropdown = get_categories_list()

time_final = time.time()
time_ejecucion = time_final - time_inicial
print('Tiempo de ejecución de get_categories_list: ',time_ejecucion)


#dropdown options for subcategory
subcategory_options = []

# Define font awesome as an external stylesheet
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css',
]

#add the external stylesheets to the app
app = Dash(__name__,external_stylesheets=external_stylesheets)


data_frame['CONTACTO'] = data_frame['CONTACTO'].astype(str)

data_frame['CONTACTO'] = data_frame['CONTACTO'].apply(lambda x: f'<i class="fas fa-envelope" title="{x}></i>')

data_frame['WEB'] = data_frame['WEB'].astype(str)

data_frame['WEB'] = data_frame['WEB'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

data_frame['Nombre de la iniciativa'] = data_frame['Nombre de la iniciativa'].astype(str)

data_frame['Nombre de la iniciativa'] = data_frame.apply(lambda row: f'<i class="fas fa-info-circle" title="{row["Función de la iniciativa"]}"></i> {row["Nombre de la iniciativa"]}', axis=1)

app.layout = html.Div([
    
    html.I(className='fas fa-info-circle', style={'font-size': '24px', 'margin-right': '10px'}),
    html.H1(children='Tabla de Datos', style={'textAlign': 'center'}),


    html.Div([    
        dcc.Dropdown(
        id='column-dropdown',
        options=categories_dropdown,
        placeholder='Seleccione una o varias categorías o subcategorías... ',
        multi=True,
        style={'width': '100%'}  
    ),], 
    style={'textAlign': 'center', 'background-color': 'lightgrey', 'display':'flex', 'justify-content':'center'}),



    dash_table.DataTable(
        id='data-table',
        data=data_frame[excluded_columns].to_dict('records'),
        columns=[
            {'id': col, 'name': 'PAIS' if col == 'CODIGO' else col, 'presentation': 'markdown'} if col in ['WEB', 'CONTACTO','Nombre de la iniciativa'] else {'id': col, 'name': col}
            for col in excluded_columns
        ],
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell={'minWidth': '50px', 'maxWidth': '250px', 'textAlign': 'left'},
        style_header={'fontWeight': 'bold', 'backgroundColor': 'lightgrey'},
        markdown_options={"html": True},

        tooltip_data=[
            {
                
            }
            for row in data_frame.to_dict('records')
            
        ],
        tooltip_duration=None,
        
        style_data_conditional=[
    {
        'if': {'column_id': 'CONTACTO'},
        'backgroundColor': '#ECECEC',
        'color': '#24BAC4',
        'cursor': 'pointer',
        'title': 'Test',
    },
    {
        'if': {'column_id': 'Nombre de la iniciativa'},
        'backgroundColor': '#ECECEC',
        'color': '#24BAC4',
        'children': [
            html.I(className='fas fa-info-circle'),
            html.Span(' ', style={'marginRight': '5px'}),
            '{Nombre de la iniciativa}',
        ],
    },
],

    )
],style={'padding': '20px'})

@app.callback(
    [
        Output('data-table', 'data'),
        Output('column-dropdown', 'options')
    ],
    [Input('column-dropdown', 'value')]
)
def update_table(selected_category): 
    if not selected_category:
        # Si no se ha seleccionado ninguna columna o se selecciona Todas, muestra todas las filas
        return data_frame[excluded_columns].to_dict('records'), categories_dropdown


    # Filtrar el dataframe en función de las columnas seleccionadas
    filtered_df = filter_data(selected_category)

    
    time_inicial = time.time()
    
    #nuevas categorias y subcategorias a partir de los datos filtrados
    new_categories_dropdown = get_categories_list_from_data_frame(filtered_df)
    
    time_final = time.time()
    time_ejecucion = time_final - time_inicial
    print('Tiempo de ejecución de get_categories_list_from_data_frame: ',time_ejecucion)

    return filtered_df[excluded_columns].to_dict('records'), new_categories_dropdown





if __name__ == '__main__':
    app.run_server(debug=True)
