from pandas import read_csv, concat, notna

from categories_and_subcategories_protocol import *

#url
url = 'https://raw.githubusercontent.com/Keynell272/Prueba/Andres_developement/full.csv'

def get_all_data():
    try:
        #get data from csv skipping first two rows and ignoring last 8 rows
        data_frame = read_csv(url, delimiter=',', encoding='utf-8', skiprows=2,skipfooter=8,engine='python',dtype={'SUBDISCIPLINES': str})
        return data_frame
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    

########################## SET CATEGORIAS ##########################
def get_categories_set():
    data_frame = get_all_data()

    if data_frame is not None:
        # extract codes
        categories = data_frame['SUBDISCIPLINES'].unique()
        # create empty set
        categories_set = set()

        # Iterate through the categories and extract the first two digits of each code
        for code in categories:
            # Check if the code is not null
            if notna(code):
                # Divide el código por comas y luego extrae los primeros dos dígitos de cada parte
                segments = [part[:2] for part in code.split(',')]
                # Agrega los primeros dos dígitos al conjunto
                categories_set.update(segments)

        return categories_set
    else:
        return set()

########################## SET SUBCATEGORIAS ##########################
def get_subcategories_set():
    data_frame = get_all_data()

    if data_frame is not None:
        # extract codes
        codes = data_frame['SUBDISCIPLINES'].unique()
        # create empty set
        subcategories_set = set()

        # Iterate through the categories and extract the first two digits of each code
        for code in codes:
            # Check if the code is not null
            if notna(code):
                # Divide el código por comas y luego extrae los primeros dos dígitos de cada parte
                segments = [part for part in code.split(',')]
                # Agrega los primeros dos dígitos al conjunto
                subcategories_set.update(segments)

        return subcategories_set
    else:
        return set()
    

########################## GET CATEGORY NAMES ##########################
def get_categories():
    categories_codes= list(get_categories_set())
    category_names = []
    for code in categories_codes:
        category_names.append(get_category_by_code(code))
    return category_names

print(get_all_data()['SUBDISCIPLINES'].unique())