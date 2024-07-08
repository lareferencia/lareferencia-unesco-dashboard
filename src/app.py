from dash import Dash, Input, Output, ctx, html
import time
from data import *
import dash_bootstrap_components as dbc

from layout import *

# Get data from the data layer
data_frame = get_all_data()

# get global lang
lang = get_language


time_inicial = time.time()

#get categories for the dropdown and check the time of execution
categories_dropdown = get_categories_list()

time_final = time.time()
time_total = time_final - time_inicial

# get objetivos unesco options and check the time of execution
unesco_options = get_categories_list_objetivos_unesco()

print('Time taken by to get categories', time_total)



# Define font awesome and bootstrap as external stylesheets
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css',
    dbc.themes.BOOTSTRAP
]

# Add external stylesheets to the Dash app instance and set the server variable to the app.server
app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout =html.Div(
    id='main-layout',
    children=[]
)
# Link the layout to the app instance and set the layout to the app.layout
app.layout.children = getLayout(categories_dropdown,data_frame,unesco_options)



############################# CALLBACKS ########################################

#callback to update the table and dropdowns based on the selected values of the dropdowns
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
    # get the time of execution of the update_table function
    time_inicial = time.time()
    # call the update_table function from the data layer
    Output = update_table(selected_category, selected_countries, selected_objetivos_unesco)
    time_final = time.time()
    time_total = time_final - time_inicial
    print('Time taken by the update_table function: ', time_total)
    return Output

#callback for the modal that shows the information of the selected cell
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
    # Check if the modal is closed by checking the trigger_id of the callback
    # the trigger_id is the id of the component that triggered the callback
    if ctx.triggered_id == "row-selection-modal-close":
        return False, None
    # Check if the cell is selected and the modal is not open
    if  selected_cell and not is_open:
        # Get the value of the selected cell
        cell_value = selected_cell['value']
        print('Selected cell ', selected_cell)
        # Check if cell_value is present in 'Nombre de la iniciativa' column
        if cell_value in data_frame['Nombre de la iniciativa'].values:
            # Get the function of the initiative from the data_frame
            function_of_initiative = data_frame.loc[data_frame['Nombre de la iniciativa'] == cell_value, 'Función de la iniciativa'].values[0]
            # Create the content of the card
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

#lang callback to set global language variable
@app.callback(
    [
        Output('language-dropdown', 'value'),
        Output('main-layout', 'children')
    ],
    [Input('language-dropdown', 'value')]
)
def set_lang(value):
    print('Inside callback set_lang')
    # case: value is empty
    if value is None or value == "":
        return ""
    set_language(value)
    # render the layout with the new language
    layout = getLayout(categories_dropdown,data_frame,unesco_options)
    return value, layout


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
