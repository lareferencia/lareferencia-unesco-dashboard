from dash import Dash, dcc, html, Input, Output, dash_table

import pandas as pd

from data import *

#from data import *


#create a data frame with the csv
data_frame = get_all_data()

#columns to display in the table
excluded_columns = ['CODIGO', 'Nombre de la iniciativa', 'WEB', 'CONTACTO']

#rest of columns (will be displayed in different dopdowns depending on the column value)
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

#Set column 'Contacto' as string
data_frame['CONTACTO'] = data_frame['CONTACTO'].astype(str)

#Concat 'Contacto' column with an icon
data_frame['CONTACTO'] = data_frame['CONTACTO'].apply(lambda x: f'<i class="fas fa-envelope"></i>')

# Set column 'WEB' as string
data_frame['WEB'] = data_frame['WEB'].astype(str)

# Convert 'WEB' column to a link
data_frame['WEB'] = data_frame['WEB'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

app.layout = html.Div([
    
    html.I(className='fas fa-info-circle', style={'font-size': '24px', 'margin-right': '10px'}),
    html.H1(children='Tabla de Datos', style={'textAlign': 'center'}),


    html.Div([    
        dcc.Dropdown(
        id='column-dropdown',
        options=categories_dropdown,
        placeholder='Seleccione una o varias categorías o subcategorías... ',
        clearable=True,
        multi=True,
        style={'width': '100%'}  
    ),], 
    style={'textAlign': 'center', 'background-color': 'lightgrey', 'display':'flex', 'justify-content':'center'}),



    dash_table.DataTable(
        id='data-table',
        data=data_frame[excluded_columns].to_dict('records'),
        columns=[
            {'id': col, 'name': col, 'presentation': 'markdown'} if col in ['WEB', 'CONTACTO'] else {'id': col, 'name': col}
            for col in excluded_columns
        ],
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell={'minWidth': '50px', 'maxWidth': '250px', 'textAlign': 'left'},
        style_header={'fontWeight': 'bold', 'backgroundColor': 'lightgrey'},
        markdown_options={"html": True},

        tooltip_data=[
            {
                'CONTACTO': {
                    'type': 'text',
                    'value': row['CONTACTO'] if pd.notna(row['CONTACTO']) else '',
                },
                'Nombre de la iniciativa': {
                    'type': 'text',
                    'value': row['Función de la iniciativa'] if pd.notna(row['Función de la iniciativa']) else '',
                },
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
