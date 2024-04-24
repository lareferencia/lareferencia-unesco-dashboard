1. Colocar en inglés todo lo que esta en español, variables, textos de print, etc.

2. Colocar en el archivo de configuración "config.ini" los strings de configuracion, por ejemplo las URL. EJEMPLO:


"En config.ini"
```
[DATA]
URL = https://raw.githubusercontent.com/lareferencia/lareferencia-unesco-dashboard/main/csv%%20files/full.csv
COUNTRY_A_CODE = https://raw.githubusercontent.com/lareferencia/lareferencia-unesco-dashboard/main/csv%%20files/codigo_a_pais.csv
```
"En data.py"
```
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

#URL
url = config['DATA']['URL']
```

