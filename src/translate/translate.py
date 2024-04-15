import os
import json

def load_json(file_name):
    current_dir = os.path.dirname(__file__)  # Directorio actual del script
    file_path = os.path.join(current_dir, file_name)

    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    return data

#load EN json 
en = load_json("en.json")
#load ES json   
es = load_json("es.json")

def translate(lang,text):
    # case: text is empty
    if text is None or text == "":
        return ""
    if lang == "en":
        return en[text]
    if lang == "es":
        return es[text]
    return text