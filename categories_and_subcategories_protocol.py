from pandas import read_csv, concat, notna

#categories_url
categories_url = 'https://raw.githubusercontent.com/Keynell272/Prueba/Andres_developement/csv%20files/Categories.csv'

#subcategories url
subcategories_url = 'https://raw.githubusercontent.com/Keynell272/Prueba/Andres_developement/csv%20files/Subcategories.csv'

def get_categories():
    try:
        # Utilizar pandas directamente para leer el CSV desde la URL
        dummy_data = read_csv(categories_url, delimiter=',', encoding='utf-8',dtype={'Código': str, 'cod_categoría': str})
        return dummy_data
    except Exception as e:
        print(f"Error loading categories: {e}")
        return None

def get_subcategories():
    try:
        # Utilizar pandas directamente para leer el CSV desde la URL
        dummy_data = read_csv(subcategories_url, delimiter=',', encoding='utf-8',dtype={'Código': str, 'cod_categoría': str})
        return dummy_data
    except Exception as e:
        print(f"Error loading subcategories: {e}")
        return None    

#get data from csv
categories = get_categories()

#get data from csv
subcategories = get_subcategories()


def get_category_by_code(code):
    filtro = categories['cod_categoría']==code
    return categories.loc[filtro,'Categoría'].values[0]


def get_code_by_category(category):
    filtro = categories['Categoría']==category
    return categories.loc[filtro,'cod_categoría'].values[0]


def get_subcategory_by_code(code):
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

def get_code_by_subcategory(subcategory):
    #get the category code
    filtro=subcategories['Subcategoría'].str.strip()==subcategory
    category_code = subcategories.loc[filtro,'cod_categoría'].values[0]
    subcategory_code = subcategories.loc[filtro,'Código'].values[0]

    return category_code + subcategory_code


def get_subcategories_by_category_code(category_code):
    filtro = subcategories['cod_categoría']==category_code
    return subcategories.loc[filtro,'Subcategoría'].values

