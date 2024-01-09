from pandas import read_csv, concat, notna

from categories_and_subcategories_protocol import *

import time

import re

#url
url = 'https://raw.githubusercontent.com/Keynell272/Prueba/Andres_developement/csv%20files/full.csv'

def cure_data(data_frame):
    # if NAN in web column, replace with 'NO INFO'
    data_frame['WEB'] = data_frame['WEB'].fillna('NO INFO')
    # if web is 'falta web' replace with 'NO INFO'
    data_frame['WEB'] = data_frame['WEB'].apply(lambda x: 'NO INFO' if x == 'falta web' else x)
    # if NAN in contact column, replace with 'NO INFO'
    data_frame['CONTACTO'] = data_frame['CONTACTO'].fillna('NO INFO')

try:
    #get data from csv skipping first two rows and ignoring last 8 rows
    data_frame = read_csv(url, delimiter=',', encoding='utf-8', skiprows=2,skipfooter=8,engine='python',dtype={'SUBDISCIPLINES': str})
    #cure data
    cure_data(data_frame)
except Exception as e:
    print(f"Error loading data: {e}")
    
def get_all_data():
    return data_frame



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
    
########################## SET CATEGORIA BY GIVEN DATA FRAME ##########################
def get_categories_set_from_data_frame(data):
    data_frame=data
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
    
########################## SET SUBCATEGORIA BY GIVEN DATA FRAME ##########################
def get_subcategories_set_from_data_frame(data):
    data_frame=data
    if data_frame is not None:
        # extract codes
        subcategories = data_frame['SUBDISCIPLINES'].unique()
        # create empty set
        subcategories_set = set()

        # Iterate through the categories and extract the first two digits of each code
        for code in subcategories:
            # Check if the code is not null
            if notna(code):
                # Divide el código por comas y luego extrae los primeros dos dígitos de cada parte
                segments = [part for part in code.split(',')]
                # Agrega los primeros dos dígitos al conjunto
                subcategories_set.update(segments)

        return subcategories_set
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
def get_category_names():

    categories_codes= list(get_categories_set())

    category_names = []

    for code in categories_codes:
        category_names.append(get_category_by_code(code))

    return category_names

def get_subcategory_names():
    subcategories_codes= list(get_subcategories_set())
    subcategory_names = []
    for code in subcategories_codes:
        subcategory_names.append(get_subcategory_by_code(code))
    return subcategory_names


########################## all categories in dictionary with code ##########################
def get_categories_list():
    categories_codes= sorted(get_categories_set(), key=lambda x: int(x))
    categories_list = []
    if categories_codes is not None:
        for code in categories_codes:
            #create label with name and count
            label = f'{get_category_by_code(code)} ({get_category_count(code)})'
            #append dictionary to the list of dictionaries
            categories_list.append({'label': label, 'value': code})
            #get subcategories for each category
            subcategories = get_subcategories_by_category_code(code)
            for subcategory in subcategories:
                code_subcategory = get_code_by_subcategory(subcategory)
                #create label with name and count
                label = f'..... {subcategory} ({get_subcategory_count(code_subcategory)})'
                #label = f'..... {subcategory} '
                #append dictionary to the list of dictionaries
                categories_list.append({'label': label, 'value': code_subcategory})
        return categories_list
    else:
        return []
    
########################## all categories in dictionary with code FROM GIVEN DATA FRAME ##########################
def get_categories_list_from_data_frame(data_frame):
    #categories_codes= list(get_categories_set_from_data_frame(data_frame))
    subcategories_codes= list(get_subcategories_set_from_data_frame(data_frame))  
    categories_codes = sorted(set([s[:2] for s in subcategories_codes]), key=lambda x: int(x))
    categories_list = []
    if categories_codes is not None:
        for code in categories_codes:
            #create label with name and count
            label = f'{get_category_by_code(code)} ({get_category_count_filtered(code,data_frame)})'
            #append dictionary to the list of dictionaries
            categories_list.append({'label': label, 'value': code})
            #get subcategories for each category
            subcategories = get_subcategories_by_category_code(code)
            for subcategory in subcategories:
                #check if subcategory code is in the subcategories codes list
                code_subcategory = get_code_by_subcategory(subcategory)
                if code_subcategory in subcategories_codes:
                    #create label with name and count
                    label = f'..... {subcategory} ({get_subcategory_count_filtered(code_subcategory,data_frame)})'
                    #label = f'..... {subcategory} '
                    #append dictionary to the list of dictionaries
                    categories_list.append({'label': label, 'value': code_subcategory})
        return categories_list
    else:
        return []


###################### get count for category ######################
def get_category_count(category):
    data_frame = get_all_data()
    if data_frame is not None:
        #get count for category
        filtro = data_frame['SUBDISCIPLINES'].apply(lambda x: any(subdisciplina.startswith(category) for subdisciplina in str(x).split(',')))
        count = len(data_frame[filtro])
        return count
    else:
        return 0

###################### get count for category with filtered data_frame ######################
def get_category_count_filtered(category,filtered_data_frame):
    data_frame = filtered_data_frame
    if data_frame is not None:
        #get count for category
        filtro = data_frame['SUBDISCIPLINES'].apply(lambda x: any(subdisciplina.startswith(category) for subdisciplina in str(x).split(',')))
        count = len(data_frame[filtro])
        return count
    else:
        return 0

###################### get count for subcategory ######################
def get_subcategory_count(subcategory):
    data_frame = get_all_data()
    if data_frame is not None:
        #get count for subcategory
        filtro = data_frame['SUBDISCIPLINES'].apply(lambda x: any(subdisciplina.startswith(subcategory) for subdisciplina in str(x).split(',')))
        count = len(data_frame[filtro])
        return count
    else:
        return 0
    
###################### get count for subcategory in filtered data frame#################
def get_subcategory_count_filtered(subcategory,filtered_data_frame):
    data_frame = filtered_data_frame
    if data_frame is not None:
        #get count for subcategory
        filtro = data_frame['SUBDISCIPLINES'].apply(lambda x: any(subdisciplina.startswith(subcategory) for subdisciplina in str(x).split(',')))
        count = len(data_frame[filtro])
        return count
    else:
        return 0


########################## Filter data exclusive (no additive) ##########################

def filter_data(categories):
    filtered_rows = get_all_data()

    for category in categories:
        filtro = filtered_rows['SUBDISCIPLINES'].apply(lambda x: any(subdisciplina.startswith(category) for subdisciplina in str(x).split(',')))

        # Aplicar el filtro al DataFrame
        filtered_rows = filtered_rows[filtro]
    
    

    return filtered_rows