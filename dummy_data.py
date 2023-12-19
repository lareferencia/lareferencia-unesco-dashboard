from pandas import read_csv, concat

#dummy url
dummy_url = 'https://raw.githubusercontent.com/Keynell272/Prueba/Andres_developement/dummy.csv'

#with dummy data
data_frame = read_csv(dummy_url, delimiter=',', encoding='utf-8')

def get_all_data():
    return data_frame

#subcategories url
subcategories_url = 'https://raw.githubusercontent.com/Keynell272/Prueba/Andres_developement/Subcategorías%20recomendaciones%20UNESCO%20-%20Hoja%201.csv'

def get_subcategories():
    try:
        # Utilizar pandas directamente para leer el CSV desde la URL
        dummy_data = read_csv(subcategories_url, delimiter=',', encoding='utf-8')
        return dummy_data
    except Exception as e:
        print(f"Error loading subcategories: {e}")
        return None

#######################################################################################################################################

def get_data_by_column(category):
    filtered_rows = data_frame[
        (data_frame[category] == category)
    ]
    return filtered_rows
   

##########################################################################################

def get_subcategory_options(selected_category):
    match selected_category:
        case '1-Conocimiento científico abierto':
            return ['Producción científica', 'Datos abiertos de investigación', 'Recursos Educativos Abiertos',
                     'Programas informáticos de código abierto y código fuente abierto','Equipos informáticos de código abierto']	
        	
        case '2-Participación abierta de los agentes sociales ':
            return ['Ciencia Ciudadana', 'Financiación Colectiva', 'Producción Colectiva','Voluntariado Científico']
        
        case '3-Diálogos abiertos con otros sistemas de conocimiento':
            return ['Pueblos Indígenas', 'Investigadores Marginados', 'Comunidades Locales']
        		
        case '4-Infraestructuras de la ciencia abierta':
            return ['Virtuales', 'Fisicas']
        	
        case '5-DIMENSIONES NO UNESCO':
            return ['Evaluación abierta de la Ciencia', 'Innovación Abierta', 'Investigación abierta y reproducible']
        		
        case '6-Cuerpos Normativos':
            return ['Nacionales', 'Institucionales']
        	
        case '7-OBJETIVOS UNESCO':
            return ['A', 'B', 'C','D','E','F']

    return []
############################## Filter ###################################################

 #No excluyente
def filter_data_additive(categories,subcategories):
    print('subcategories : ', subcategories)
    #filter data set to an empty data frame
    filtered_rows = None
    # Loop through the columns to get the data
    for col in categories:
        current_data = get_data_by_column(col)
         # Concatenate the current_data with the existing filtered_rows
        filtered_rows = concat([filtered_rows, current_data])  
    #loop through the subcategories
    if subcategories:
        for col in subcategories:
            current_data = get_data_by_column(col)
            # Concatenate the current_data with the existing filtered_rows
            filtered_rows = concat([filtered_rows, current_data])


    # Drop duplicates from the concatenated DataFrame
    filtered_rows = filtered_rows.drop_duplicates()

    return filtered_rows

#excluyente
def filter_data(categories, subcategories):
    print('subcategories : ', subcategories)

    # Inicializar DataFrame para almacenar filas filtradas
    filtered_rows = data_frame.copy()

    # Filtrar por categorías
    for col in categories:
        filtered_rows = filtered_rows[filtered_rows[col].isin([col])]

    # Filtrar por subcategorías
    if subcategories:
        for col in subcategories:
            filtered_rows = filtered_rows[filtered_rows[col].isin([col])]

    return filtered_rows
##########################################################################################

########################## Get grouped subcategories #####################################
def get_grouped_subcategories(categories):
    # Initialize an empty list to store subcategories
    subcategories = []

    # Loop through the columns to get the data
    for col in categories:
        current_data = get_subcategory_options(col)
        
        # Create a list of dictionaries with 'label' and 'value' keys
        current_subcategories = [{'label': subcategory, 'value': subcategory} for subcategory in current_data]

        # Extend the main list with the current_subcategories
        subcategories.extend(current_subcategories)

    # Remove duplicates by converting the list to a set and back to a list
    subcategories = list({subcategory['value']: subcategory for subcategory in subcategories}.values())

    return subcategories
