from dash import Dash, Input, Output, ctx, html
import time
from data import *
import dash_bootstrap_components as dbc

from layout import getLayout

# Obtener datos desde la capa de datos
data_frame = get_all_data()



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

app.layout = getLayout(categories_dropdown,data_frame,unesco_options)

@app.callback(
    [
        Output('data-table', 'rowData'),
        Output('column-dropdown', 'options'),
        Output('countries-dropdown', 'options'),
        Output('objetivos-dropdown', 'options')
    ],
    [Input('column-dropdown', 'value'),
     Input('countries-dropdown', 'value'),
     Input('objetivos-dropdown', 'value')]
)
def callback_update_table(selected_category, selected_countries, selected_objetivos_unesco):
    # estimar el tiempo de ejecución de la función
    time_inicial = time.time()
    Output = update_table(selected_category, selected_countries, selected_objetivos_unesco)
    time_final = time.time()
    time_ejecucion = time_final - time_inicial
    print('Tiempo de ejecución de update_table: ', time_ejecucion)
    return Output

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
