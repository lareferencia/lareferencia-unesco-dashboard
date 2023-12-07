#pandas
from pandas import read_csv


#read csv from this folder
data_frame = read_csv('Modelo coma.csv', delimiter=',', encoding='utf-8')

#print rows where column '2-Participación abierta de los agentes sociales' is equal to '2-Participación abierta de los agentes sociales'



filtered_rows = data_frame[
    (data_frame['2-Participación abierta de los agentes sociales '] == '2-Participación abierta de los agentes sociales ') &
    (data_frame['Ciencia Ciudadana'] == 'Ciencia Ciudadana')
]
print(filtered_rows)



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