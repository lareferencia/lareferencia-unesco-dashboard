import configparser
from pandas import read_csv, concat, notna
from categories_and_subcategories_protocol import *
from utilities.logging_utils import log_execution_time
# up one level up to import the translate function
from translate.translate import translate


config = configparser.ConfigParser()
config.read('config.ini')

#URL
url = config['DATA']['URL']

#load codigo_a_pais from csv
codigo_a_pais = read_csv(config['DATA']['COUNTRY_A_CODE'])

#Seleccionar columnas a mostrar en el grid
excluded_columns = ['PAIS', 'Nombre de la iniciativa','Detalles', 'WEB', 'CONTACTO']

@log_execution_time
def cure_data(data_frame):
    # if NAN in web column, replace with 'NO INFO'
    data_frame['WEB'] = data_frame['WEB'].fillna('NO INFO')
    # if web is 'falta web' replace with 'NO INFO'
    data_frame['WEB'] = data_frame['WEB'].apply(lambda x: 'NO INFO' if x == 'falta web' else x)
    # if NAN in contact column, replace with 'NO INFO'
    data_frame['CONTACTO'] = data_frame['CONTACTO'].fillna('NO INFO')
    # Modify the column name 'CODIGO' to 'PAIS'
    data_frame.rename(columns={'CODIGO': 'PAIS'}, inplace=True)

    # Replace the country codes with the country names
    data_frame['PAIS'] = data_frame['PAIS'].apply(lambda x: codigo_a_pais[codigo_a_pais['Codigo'] == x]['Pais'].values[0] if x in codigo_a_pais['Codigo'].values else x)

    # Add a new column called 'Detalles' which is the same as 'Nombre de la iniciativa'
    data_frame['Detalles'] = data_frame['Nombre de la iniciativa']
    

try:
    #get data from csv skipping first two rows and ignoring last 8 rows
    data_frame = read_csv(url, delimiter=',', encoding='utf-8', skiprows=2,skipfooter=8,engine='python',dtype={'SUBDISCIPLINES': str})
    #cure data
    cure_data(data_frame)
except Exception as e:
    print(f"Error loading data: {e}")

@log_execution_time    
def get_all_data():
    return data_frame



#TODO: CAMBIAR LOS NOMBRES QUE ESTAN EN ESPAÑOL A INGLÉS

########################## SET CATEGORIES ##########################
@log_execution_time
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
                # Split the code by commas and then extract the first two digits of each part
                segments = [part[:2] for part in code.split(',')]
                # update the set with the first two digits of the code
                categories_set.update(segments)

        return categories_set
    else:
        return set()
    
########################## SET CATEGORY BY GIVEN DATA FRAME ##########################
@log_execution_time
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
                # Split the code by commas and then extract the first two digits of each part
                segments = [part[:2] for part in code.split(',')]
                # Update the set with the first two digits of the code
                categories_set.update(segments)

        return categories_set
    else:
        return set()
    
########################## SET SUBCATEGORY BY GIVEN DATA FRAME ##########################
@log_execution_time
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
                # Split the code by commas and then extract the first two digits of each part
                segments = [part for part in code.split(',')]
                # Update the set with the first two digits of the code
                subcategories_set.update(segments)

        return subcategories_set
    else:
        return set()

########################## SET SUBCATEGORIES ##########################
@log_execution_time
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
                # Split the code by commas and then extract the first two digits of each part
                segments = [part for part in code.split(',')]
                # Update the set with the first two digits of the code
                subcategories_set.update(segments)

        return subcategories_set
    else:
        return set()
    
########################## GET CATEGORY NAMES ##########################
@log_execution_time
def get_category_names():
    # get categories codes
    categories_codes= list(get_categories_set())
    # create empty list
    category_names = []
    # iterate through the categories codes
    for code in categories_codes:
        # append the category name to the list
        category_names.append(get_category_by_code(code))

    return category_names

########################## GET SUBCATEGORY NAMES ##########################
@log_execution_time
def get_subcategory_names():
    # get subcategories codes
    subcategories_codes= list(get_subcategories_set())
    # create empty list
    subcategory_names = []
    # iterate through the subcategories codes
    for code in subcategories_codes:
        # append the subcategory name to the list
        subcategory_names.append(get_subcategory_by_code(code))
        
    return subcategory_names

########################## all categories in dictionary with code ##########################
@log_execution_time
def get_categories_list(lang):
    # get categories codes sorted by code
    categories_codes= sorted(get_categories_set(), key=lambda x: int(x))
    # create empty list
    categories_list = []
    
    if categories_codes is not None:
        # iterate through the categories codes
        for code in categories_codes:
            # check if the code is not '07' (UNESCO objectives)
            if code != '07':
                #create label with name and count
                label = f'{translate(lang,get_category_by_code(code))} ({get_category_count(code)})'
                #append dictionary to the list of dictionaries
                categories_list.append({'label': label, 'value': code})
                #get subcategories for each category
                subcategories = get_subcategories_by_category_code(code)
                # iterate through the subcategories and extract the code
                for subcategory in subcategories:
                    code_subcategory = get_code_by_subcategory(subcategory)
                    #create label with name and count
                    label = f'..... {translate(lang,subcategory)} ({get_subcategory_count(code_subcategory)})'
                    #label = f'..... {subcategory} '
                    #append dictionary to the list of dictionaries
                    categories_list.append({'label': label, 'value': code_subcategory})
        return categories_list
    else:
        return []

########################## just OBJETIVOS UNESCO with subcategories in dictionary with code ##########################
@log_execution_time
def get_categories_list_objetivos_unesco(lang):
    # get subcategories for category code '07' (UNESCO objectives)
    subcategories = get_subcategories_by_category_code('07')
    subcategories_list = []
    # iterate through the subcategories and extract the code
    for subcategory in subcategories:
        code_subcategory = get_code_by_subcategory(subcategory)
        # create label with name and count
        label = f'{translate(lang,subcategory)} ({get_subcategory_count(code_subcategory)})'
        subcategories_list.append({'label': label, 'value': code_subcategory})
    return subcategories_list
    
########################## all categories in dictionary with code FROM GIVEN DATA FRAME ##########################
@log_execution_time
def get_categories_list_from_data_frame(data_frame,lang):
    #categories_codes= list(get_categories_set_from_data_frame(data_frame))
    subcategories_codes= list(get_subcategories_set_from_data_frame(data_frame)) 
    # get categories codes sorted by code 
    categories_codes = sorted(set([s[:2] for s in subcategories_codes]), key=lambda x: int(x))
    categories_list = []
    if categories_codes is not None:
        # iterate through the categories codes
        for code in categories_codes:
            if code != '07':
                #create label with name and count
                label = f'{translate(lang,get_category_by_code(code))} ({get_category_count_filtered(code,data_frame)})'
                #append dictionary to the list of dictionaries
                categories_list.append({'label': label, 'value': code})
                #get subcategories for each category
                subcategories = get_subcategories_by_category_code(code)
                for subcategory in subcategories:
                    #check if subcategory code is in the subcategories codes list
                    code_subcategory = get_code_by_subcategory(subcategory)
                    if code_subcategory in subcategories_codes:
                        #create label with name and count
                        label = f'..... {translate(lang,subcategory)} ({get_subcategory_count_filtered(code_subcategory,data_frame)})'
                        #label = f'..... {subcategory} '
                        #append dictionary to the list of dictionaries
                        categories_list.append({'label': label, 'value': code_subcategory})
        return categories_list
    else:
        return []

########################## just Objetivos unesco with subcategories FROM GIVEN DATA FRAME ##########################
@log_execution_time
def get_categories_list_objetivos_unesco_from_data_frame(data_frame,lang):
    # get subcategories for category code '07' (UNESCO objectives)
    subcategories = get_subcategories_by_category_code('07')
    subcategories_list = []
    # iterate through the subcategories and extract the code
    for subcategory in subcategories:
        code_subcategory = get_code_by_subcategory(subcategory)
        # create label with name and count
        label = f'{translate(lang,subcategory)} ({get_subcategory_count_filtered(code_subcategory,data_frame)})'
        subcategories_list.append({'label': label, 'value': code_subcategory})
    return subcategories_list

###################### get count for category ######################
@log_execution_time
def get_category_count(category):
    data_frame = get_all_data()
    if data_frame is not None:
        #get count for category with lambda function that checks if the category is in the subdisciplines
        filtro = data_frame['SUBDISCIPLINES'].apply(lambda x: any(subdisciplina.startswith(category) for subdisciplina in str(x).split(',')))
        count = len(data_frame[filtro])
        return count
    else:
        return 0

###################### get count for category with filtered data_frame ######################
@log_execution_time
def get_category_count_filtered(category,filtered_data_frame):
    # In this case data_frame is the filtered data frame and not the global data frame
    data_frame = filtered_data_frame
    if data_frame is not None:
        #get count for category with lambda function that checks if the category is in the subdisciplines
        filtro = data_frame['SUBDISCIPLINES'].apply(lambda x: any(subdisciplina.startswith(category) for subdisciplina in str(x).split(',')))
        # get count of rows that match the filter
        count = len(data_frame[filtro])
        return count
    else:
        return 0

###################### get count for subcategory ######################
@log_execution_time
def get_subcategory_count(subcategory):
    data_frame = get_all_data()
    if data_frame is not None:
        #get count for subcategory with lambda function that checks if the subcategory is in the subdisciplines
        filtro = data_frame['SUBDISCIPLINES'].apply(lambda x: any(subdisciplina.startswith(subcategory) for subdisciplina in str(x).split(',')))
        # get count of rows that match the filter
        count = len(data_frame[filtro])
        return count
    else:
        return 0
    
###################### get count for subcategory in filtered data frame#################
@log_execution_time
def get_subcategory_count_filtered(subcategory,filtered_data_frame):
    # In this case data_frame is the filtered data frame and not the global data frame
    data_frame = filtered_data_frame
    if data_frame is not None:
        #get count for subcategory
        filtro = data_frame['SUBDISCIPLINES'].apply(lambda x: any(subdisciplina.startswith(subcategory) for subdisciplina in str(x).split(',')))
        # get count of rows that match the filter
        count = len(data_frame[filtro])
        return count
    else:
        return 0


########################## Filter data exclusive (no additive) ##########################
@log_execution_time
def filter_data(categories):
    filtered_rows = get_all_data()

    # Iterate through the categories and apply the filter to the data frame
    for category in categories:
        filtro = filtered_rows['SUBDISCIPLINES'].apply(lambda x: any(subdisciplina.startswith(category) for subdisciplina in str(x).split(',')))

        # Aplicar el filtro al DataFrame
        filtered_rows = filtered_rows[filtro]
    
    

    return filtered_rows

####################### Filter data from given data frame exclusive (no additive) ############################
@log_execution_time
def filter_data_from_data_frame(categories,data_frame):
    # In this case data_frame is the filtered data frame and not the global data frame
    filtered_rows = data_frame

    for category in categories:
        filtro = filtered_rows['SUBDISCIPLINES'].apply(lambda x: any(subdisciplina.startswith(category) for subdisciplina in str(x).split(',')))

        # Aplicar el filtro al DataFrame
        filtered_rows = filtered_rows[filtro]
    
    

    return filtered_rows

@log_execution_time
def update_table(selected_category,selected_countries,selected_unesco_cat,lang):
    # case: no filters at all
    if not selected_category and not selected_countries and not selected_unesco_cat:
        new_categories_dropdown = get_categories_list(lang)
        new_categories_dropdown_unesco = get_categories_list_objetivos_unesco(lang)
        new_countries_dropdown = data_frame['PAIS'].unique()
        return data_frame[excluded_columns].to_dict('records'), new_categories_dropdown, new_countries_dropdown, new_categories_dropdown_unesco
    
    # case: filter by countries but not by categories or unesco objectives
    if not selected_category and selected_countries and not selected_unesco_cat:
        filtered_df = data_frame[data_frame['PAIS'].isin(selected_countries)]
        # new categories and subcategories from filtered data
        new_categories_dropdown = get_categories_list_from_data_frame(filtered_df,lang)
        new_categories_dropdown_unesco = get_categories_list_objetivos_unesco_from_data_frame(filtered_df,lang)
        return filtered_df[excluded_columns].to_dict('records'), new_categories_dropdown, filtered_df['PAIS'].unique(), new_categories_dropdown_unesco
    
    # case: filter by categories but not by countries or unesco objectives
    if selected_category and not selected_countries and not selected_unesco_cat:
        filtered_df = filter_data(selected_category)
        # new categories and subcategories from filtered data
        new_categories_dropdown = get_categories_list_from_data_frame(filtered_df,lang)
        new_categories_dropdown_unesco = get_categories_list_objetivos_unesco_from_data_frame(filtered_df,lang)
        return filtered_df[excluded_columns].to_dict('records'), new_categories_dropdown, filtered_df['PAIS'].unique(), new_categories_dropdown_unesco
    
    # case: filter by categories and countries but not by unesco objectives
    if selected_category and selected_countries and not selected_unesco_cat:
        # apply country filter before category filter
        filtered_df = data_frame[data_frame['PAIS'].isin(selected_countries)]
        # apply category filter after country filter
        filtered_df = filter_data_from_data_frame(selected_category, filtered_df)
        # new categories and subcategories from filtered data
        new_categories_dropdown = get_categories_list_from_data_frame(filtered_df,lang)
        new_categories_dropdown_unesco = get_categories_list_objetivos_unesco_from_data_frame(filtered_df,lang)
        return filtered_df[excluded_columns].to_dict('records'), new_categories_dropdown, filtered_df['PAIS'].unique(), new_categories_dropdown_unesco
    
    # case: filter by unesco objectives but not by categories or countries
    if not selected_category and not selected_countries and selected_unesco_cat:
        filtered_df = filter_data(selected_unesco_cat)
        # new categories and subcategories from filtered data
        new_categories_dropdown = get_categories_list_from_data_frame(filtered_df,lang)
        new_categories_dropdown_unesco = get_categories_list_objetivos_unesco_from_data_frame(filtered_df,lang)
        return filtered_df[excluded_columns].to_dict('records'), new_categories_dropdown, filtered_df['PAIS'].unique(), new_categories_dropdown_unesco
    
    # case: filter by unesco objectives and countries but not by categories
    if not selected_category and selected_countries and selected_unesco_cat:
        # apply country filter before category filter
        filtered_df = data_frame[data_frame['PAIS'].isin(selected_countries)]
        # apply category filter after country filter
        filtered_df = filter_data_from_data_frame(selected_unesco_cat, filtered_df)
        # new categories and subcategories from filtered data
        new_categories_dropdown = get_categories_list_from_data_frame(filtered_df,lang)
        new_categories_dropdown_unesco = get_categories_list_objetivos_unesco_from_data_frame(filtered_df,lang)
        return filtered_df[excluded_columns].to_dict('records'), new_categories_dropdown, filtered_df['PAIS'].unique(), new_categories_dropdown_unesco
    
    # case: filter by unesco objectives and categories but not by countries
    if selected_category and not selected_countries and selected_unesco_cat:
        filtered_df = filter_data_from_data_frame(selected_unesco_cat, data_frame)
        # apply category filter after country filter
        filtered_df = filter_data_from_data_frame(selected_category, filtered_df)
        # new categories and subcategories from filtered data
        new_categories_dropdown = get_categories_list_from_data_frame(filtered_df,lang)
        new_categories_dropdown_unesco = get_categories_list_objetivos_unesco_from_data_frame(filtered_df,lang)
        return filtered_df[excluded_columns].to_dict('records'), new_categories_dropdown, filtered_df['PAIS'].unique(), new_categories_dropdown_unesco
    
    # case: filter by unesco objectives, categories and countries
    if selected_category and selected_countries and selected_unesco_cat:
        # apply country filter before category filter
        filtered_df = data_frame[data_frame['PAIS'].isin(selected_countries)]
        # apply category filter after country filter
        filtered_df = filter_data_from_data_frame(selected_category, filtered_df)
        # apply unesco objectives filter after category filter
        filtered_df = filter_data_from_data_frame(selected_unesco_cat, filtered_df)
        # new categories and subcategories from filtered data
        new_categories_dropdown = get_categories_list_from_data_frame(filtered_df,lang)
        new_categories_dropdown_unesco = get_categories_list_objetivos_unesco_from_data_frame(filtered_df,lang)
        return filtered_df[excluded_columns].to_dict('records'), new_categories_dropdown, filtered_df['PAIS'].unique(), new_categories_dropdown_unesco
    
    #