from dash import Dash, dcc, html, Input, Output, dash_table

from data import *


#create a data frame with the csv
data_frame = get_all_data()

#columns to display in the table
excluded_columns = ['Pais', 'Nombre de la iniciativa', 'Descripción', 'Sitio web', 'Correo contacto']

#rest of columns (will be displayed in different dopdowns depending on the column value)
rest_columns = data_frame.columns[5:]

categories_dropdown = rest_columns[rest_columns.str.match(r'\d+')]
#add option 'Todas' to the dropdown
#categories_dropdown =categories_dropdown.tolist() + ['Todas']


#dropdown options for subcategory
subcategory_options = []


app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Tabla de Datos', style={'textAlign': 'center'}),

        dcc.Checklist(
        id='additive-switch',
        options=[
            {'label': 'Aditivo', 'value': True}
        ],
        value=[]
    ),

    html.Div([    
        dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col} for col in categories_dropdown],
        placeholder='Seleccione una o varias categorías ... ',
        clearable=True,
        multi=True,
        style={'width': '100%'}  
    ),

    dcc.Dropdown(
        id='subcategory-dropdown',
        options=[{'label': subcategory, 'value': subcategory} for subcategory in subcategory_options],
        placeholder='Seleccione una o varias sub-categorías ... ',
        clearable=True,  
        multi=True,
        style={'width': '100%'}  
    )], 
    style={'textAlign': 'center', 'background-color': 'lightgrey', 'display':'flex', 'justify-content':'center'}),



    dash_table.DataTable(
        id='data-table',
        data=data_frame[excluded_columns].to_dict('records'),
        columns=[{'name': col, 'id': col} for col in excluded_columns],
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell={'minWidth': '150px', 'width': '150px', 'maxWidth': '150px'},
        style_header={'fontWeight': 'bold', 'backgroundColor': 'lightgrey'},
    )
])

@app.callback(
    [Output('data-table', 'data'),
     Output('subcategory-dropdown', 'options')],
    [Input('column-dropdown', 'value'),
     Input('subcategory-dropdown', 'value'),
     Input('additive-switch', 'value')]
)
def update_table(selected_category, selected_subcategory,additive_switch):
    #extract value from the checklist
    if additive_switch:
        print ('additive_switch : ', additive_switch[0])
    print('selected categories : ', selected_category)
    print('selected subcategories : ', selected_subcategory)
    if not selected_category:
        # Si no se ha seleccionado ninguna columna o se selecciona Todas, muestra todas las filas
        return data_frame[excluded_columns].to_dict('records'),[]

    #filter the data with the values selected in the dropdowns
    filtered_df = filter_data_additive(selected_category, selected_subcategory) if additive_switch else filter_data(selected_category, selected_subcategory)

    # Obtiene las subcategorías de la columna seleccionada
    subcategory_options = get_grouped_subcategories(selected_category)

    print('Fitered on dashboard : \n', filtered_df)

    return filtered_df[excluded_columns].to_dict('records'),subcategory_options




if __name__ == '__main__':
    app.run_server(debug=True)
