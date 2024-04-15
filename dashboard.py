from dash import Dash, Input, Output, ctx
import time
from data import *
import dash_bootstrap_components as dbc

from layout import getLayout

# Obtener datos desde la capa de datos
data_frame = get_all_data()

#Seleccionar columnas a mostrar en el grid
excluded_columns = ['PAIS', 'Nombre de la iniciativa','Detalles', 'WEB', 'CONTACTO']

time_inicial = time.time()

#obtener categorias desde la capa de datos y medir el tiempo de consulta
categories_dropdown = get_categories_list()

time_final = time.time()
time_ejecucion = time_final - time_inicial

unesco_options = get_categories_list_objetivos_unesco()

print('Tiempo de ejecución de get_categories_list: ', time_ejecucion)



# Define font awesome y los temas de bootstrap como hojas de estilo externas usadas en la aplicación
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css',
    dbc.themes.BOOTSTRAP
]

# Agregar las hojas de estilo externas a la aplicación
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = getLayout(categories_dropdown,excluded_columns,data_frame,unesco_options)

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
        cell_value = selected_cell['value']
        print('Selected cell ', selected_cell)
        # Check if cell_value is present in 'Nombre de la iniciativa' column
        if cell_value in data_frame['Nombre de la iniciativa'].values:
            function_of_initiative = data_frame.loc[data_frame['Nombre de la iniciativa'] == cell_value, 'Función de la iniciativa'].values[0]
            card_content = [
                html.H4(str(cell_value), style={'color': 'white', 'background-color': '#007BFF', 'padding': '10px'}),
                html.P(function_of_initiative, style={'margin': '10px'}),
                html.Hr(),
                html.Div([
                    html.Strong('País: '),
                    html.Span(str(data_frame.loc[data_frame['Nombre de la iniciativa'] == cell_value, 'PAIS'].values[0]))
                ], style={'margin': '10px'}),
                html.Div([
                    html.Strong('Web: '),
                    html.Span(str(data_frame.loc[data_frame['Nombre de la iniciativa'] == cell_value, 'WEB'].values[0]))
                ], style={'margin': '10px'}),
                html.Div([
                    html.Strong('Contacto: '),
                    html.Span(str(data_frame.loc[data_frame['Nombre de la iniciativa'] == cell_value, 'CONTACTO'].values[0]))
                ], style={'margin': '10px'})]
            return True, card_content
        else:
            return False, []
    return False, []





if __name__ == '__main__':
    app.run_server(debug=True)
