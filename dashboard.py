from dash import Dash, dcc, html, Input, Output, dash_table

import pandas as pd

from data import *

#get data
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
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'
]

#add the external stylesheets to the app
app = Dash(__name__,external_stylesheets=external_stylesheets)

#display settings in data_frame
data_frame['CONTACTO'] = data_frame['CONTACTO'].astype(str)

#add icon to contact column if different to NO INFO
data_frame['CONTACTO'] = data_frame['CONTACTO'].apply(lambda x: f'<i class="fas fa-envelope" title="{x}"></i>' if x != 'NO INFO' else x)

data_frame['WEB'] = data_frame['WEB'].astype(str)

#hiperlink to web column if different to NO INFO
data_frame['WEB'] = data_frame['WEB'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>' if x != 'NO INFO' else x)

data_frame['Nombre de la iniciativa'] = data_frame['Nombre de la iniciativa'].astype(str)

#columna adicional con el tooltip a la celda
data_frame['Nombre de la iniciativa_tooltip'] = data_frame.apply(
    lambda row: f'{row["Nombre de la iniciativa"]}: {row["Función de la iniciativa"]}',
    axis=1
)

data_frame['Nombre de la iniciativa'] = data_frame.apply(
    lambda row: f'<i class="fas fa-info-circle"></i> {row["Nombre de la iniciativa"]}', 
    axis=1
)


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
            style={'background-color':'#cefad0','width': '100%'}
            )], 
    style={'textAlign': 'center', 'background-color': 'lightgrey', 'display':'flex', 'justify-content':'center','flex-direction':'column'}),



    dash_table.DataTable(
        id='data-table',
        data=data_frame[excluded_columns].to_dict('records'),
        columns=[
            {'id': col, 'name': 'PAIS' if col == 'CODIGO' else col, 'presentation': 'markdown'} if col in ['WEB', 'CONTACTO','Nombre de la iniciativa'] else {'id': col, 'name': col}
            for col in excluded_columns
        ],
        fixed_rows={'headers': True},
        filter_action='native',
        filter_options={"placeholder_text": "Filtrar..."},     
        page_size=20,
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell={'minWidth': '50px', 'maxWidth': '250px', 'textAlign': 'left'},
        style_header={'fontWeight': 'bold', 'backgroundColor': 'lightgrey'},
        markdown_options={"html": True},
        

    tooltip_data=[
        {
            col: {'value': str(row['Nombre de la iniciativa_tooltip']), 'type': 'markdown'}
            for col in excluded_columns if col == 'Nombre de la iniciativa'
        }
        for row in data_frame.to_dict('records')
    ],
        tooltip_duration=None,
        
        
        style_data_conditional=[
    {
        'if': {'column_id': 'CONTACTO'},
        'color': '#24BAC4',
        'cursor': 'pointer',
        'title': 'Test',
    },
    
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(220, 220, 220)',
    },
    
    {
        'if': {'column_id': 'Nombre de la iniciativa'},
        'color': '#24BAC4',
        'tooltip': {
            'type':'html'
        }
    },
],  

    )
],style={'padding': '20px'})

@app.callback(
    [
        Output('data-table', 'data'),
        Output('column-dropdown', 'options'),
        Output('countries-dropdown', 'options')
    ],
    [Input('column-dropdown', 'value'),
     Input('countries-dropdown', 'value')]
)
def update_table(selected_category,selected_countries): 
    #caso en el que no haya filtrado
    if not selected_category and not selected_countries:
        print('No hay filtros')
        # Si no se ha seleccionado ninguna columna o se selecciona Todas, muestra todas las filas
        return data_frame[excluded_columns].to_dict('records'), categories_dropdown, data_frame['PAIS'].unique()

    #caso en el que haya filtrado por paises pero no por categorias
    if not selected_category and selected_countries:
        print('Filtrado por paises')
        filtered_df = data_frame[data_frame['PAIS'].isin(selected_countries)]
        #nuevas categorias y subcategorias a partir de los datos filtrados
        new_categories_dropdown = get_categories_list_from_data_frame(filtered_df)
        return filtered_df[excluded_columns].to_dict('records'), new_categories_dropdown, filtered_df['PAIS'].unique()
    
    #caso en el que haya filtrado por categorias pero no por paises
    if selected_category and not selected_countries:
        print('Filtrado por categorias')
        filtered_df = filter_data(selected_category)
        #nuevas categorias y subcategorias a partir de los datos filtrados
        new_categories_dropdown = get_categories_list_from_data_frame(filtered_df)
        return filtered_df[excluded_columns].to_dict('records'), new_categories_dropdown, filtered_df['PAIS'].unique()
    
    #caso en el que haya filtrado por categorias y paises
    print('Filtrado por categorias y paises')
    time_inicial = time.time()
    #pasar el filtro de pais antes de filtrar por categorias
    filtered_df = data_frame[data_frame['PAIS'].isin(selected_countries)]
    
    #pasar el filtro de categorias despues de filtrar por paises
    filtered_df = filter_data_from_data_frame(selected_category,filtered_df)
    
    #nuevas categorias y subcategorias a partir de los datos filtrados
    new_categories_dropdown = get_categories_list_from_data_frame(filtered_df)
    
    time_final = time.time()
    time_ejecucion = time_final - time_inicial
    print('Tiempo de ejecución de callback: ',time_ejecucion)
    

    return filtered_df[excluded_columns].to_dict('records'), new_categories_dropdown, filtered_df['PAIS'].unique()





if __name__ == '__main__':
    app.run_server(debug=True)
