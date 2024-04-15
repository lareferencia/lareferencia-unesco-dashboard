from os.path import exists
import json

#load EN json 
with open("translate/en.json", "r", encoding='utf-8') as f:
    en = json.load(f)

#load ES json
with open("translate/es.json", "r", encoding='utf-8') as f:
    es = json.load(f)

def translate(lang,text):
    # case: text is empty
    if text is None or text == "":
        return ""
    if lang == "en":
        return en[text]
    if lang == "es":
        return es[text]
    return text