from dummy_data import *
def get_categories_by_code(code):
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

def get_subcategories_by_code(code):
    match code:
        case '01':
            return 'Texto 01'
        case '02':
            return 'Texto 02'
        case '03':
            return 'Texto 03'
    return None

subcategories = get_subcategories()

print(subcategories)