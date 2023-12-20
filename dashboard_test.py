#pandas
from pandas import read_csv, concat

from categories_and_subcategories_protocol import *

#read csv from this folder
""" data_frame = read_csv('Modelo coma.csv', delimiter=',', encoding='utf-8')

#print rows where column '2-Participación abierta de los agentes sociales' is equal to '2-Participación abierta de los agentes sociales'

columns_to_filter = ['6-Cuerpos Normativos', '3-Diálogos abiertos con otros sistemas de conocimiento']

def get_data_by_category(category):
    filtered_rows = data_frame[
        (data_frame[category] == category)
    ]
    return filtered_rows


# Initialize a condition to True
combined_condition = None

#filter data set to an empty data frame
filtered_rows = None

# Loop through the columns to get the data
for col in columns_to_filter:
    current_data = get_data_by_category(col)
    
    # Concatenate the current_data with the existing filtered_rows
    filtered_rows = concat([filtered_rows, current_data])

# Drop duplicates from the concatenated DataFrame
filtered_rows = filtered_rows.drop_duplicates()


# Filter the DataFrame based on the combined condition
#filtered_rows = data_frame[combined_condition]

print('Array categories filtration : \n',filtered_rows[['Pais','Nombre de la iniciativa']]) """

""" filtered_rows = data_frame[
    (data_frame['2-Participación abierta de los agentes sociales '] == '2-Participación abierta de los agentes sociales ') &
    (data_frame['Ciencia Ciudadana'] == 'Ciencia Ciudadana')
]
print(filtered_rows) """



#filter with regex
#print('Columns -> ',data_frame.columns[data_frame.columns.str.match(r'\d+')])


#excluded_columns = ['Pais', 'Nombre de la iniciativa', 'Descripción', 'Sitio web', 'Correo contacto']

#rest of columns (will be displayed in different dopdowns depending on the column value)
#rest_columns = data_frame.columns[5:]

#columns for the first categories dropdown
#categories_dropdown = rest_columns[rest_columns.str.match(r'\d+')]
#print(categories_dropdown)




#print columns length
#print(data_frame.columns.values)



########################## Refactorzación de código #####################################

""" #address where the csv is located
url = 'https://raw.githubusercontent.com/Keynell272/Prueba/Andres_developement/dummy.csv'

#read csv from this folder
data_frame = read_csv(url, delimiter=',', encoding='utf-8')
#extract codes
categories = data_frame['Subcategorías'].unique()
#create empty set
categories_set = set()
# Itera sobre cada código en la columna 'Subcategorías'
for code in categories:
    # Divide el código por comas y luego extrae los primeros dos dígitos de cada parte
    segments = [part[:2] for part in code.split(',')]
    # Agrega los primeros dos dígitos al conjunto
    categories_set.update(segments)

categories_codes= list(categories_set)    
category_names = []
for code in categories_codes:
    category_names.append(get_category_by_code(code))


print('Categories : ', categories)    
print('codes : ', categories_set)
print('category names : ', category_names)
 """
from new_data import *

df = get_all_data()

filtro = df['SUBDISCIPLINES'].apply(lambda x: any(subdisciplina.startswith('03') for subdisciplina in str(x).split(',')))

# Aplicar el filtro al DataFrame
df_filtrado = df[filtro]

print(df_filtrado)