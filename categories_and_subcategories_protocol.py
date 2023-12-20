from dummy_data import *

#subcategories url
subcategories_url = 'https://raw.githubusercontent.com/Keynell272/Prueba/Andres_developement/Subs.csv'

def get_subcategories():
    try:
        # Utilizar pandas directamente para leer el CSV desde la URL
        dummy_data = read_csv(subcategories_url, delimiter=',', encoding='utf-8',dtype={'Código': str, 'cod_categoría': str})
        return dummy_data
    except Exception as e:
        print(f"Error loading subcategories: {e}")
        return None

#get data from csv
subcategories = get_subcategories()

def get_category_by_code(code):
    match code:
        case '01':
            return 'Conocimiento científico abierto'
        case '02':
            return 'Participación abierta de los agentes sociales '
        case '03':
            return 'Diálogos abiertos con otros sistemas de conocimiento'
        case '04':
            return 'Infraestructuras de la ciencia abierta'
        case '05':
            return 'DIMENSIONES NO UNESCO'
        case '06':
            return 'Cuerpos Normativos'
        case '07':
            return 'OBJETIVOS UNESCO'
    return None

def get_code_by_category(category):
    match category:
        case 'Conocimiento científico abierto':
            return '01'
        case 'Participación abierta de los agentes sociales ':
            return '02'
        case 'Diálogos abiertos con otros sistemas de conocimiento':
            return '03'
        case 'Infraestructuras de la ciencia abierta':
            return '04'
        case 'DIMENSIONES NO UNESCO':
            return '05'
        case 'Cuerpos Normativos':
            return '06'
        case 'OBJETIVOS UNESCO':
            return '07'
    return None

def get_subcategories_by_code(code):
    #slice the code to get the category code
    category_code = code[:2]
    #slice the code to get the subcategory code
    sub_code = code[2:]
    filtro = (subcategories['Código']==sub_code) & (subcategories['cod_categoría']==category_code)
    if len(subcategories.loc[filtro,'Subcategoría'].values) > 0:
        return subcategories.loc[filtro,'Subcategoría'].values[0]  
    else:
        print('No se encontró la subcategoría para el codigo -> ',code)
        return None

