from pandas import read_csv, concat

from categories_and_subcategories_protocol import *

#url
url = 'https://raw.githubusercontent.com/Keynell272/Prueba/Andres_developement/2023%20Estado%20del%20cumplimiento%20de%20recomendaciones%20UNESCO%20en%20países%20miembros%20de%20LA%20Referencia.xlsx%20-%20Todo.csv'

#get data from csv
data_frame = read_csv(url, delimiter=',', encoding='utf-8')

print(data_frame)