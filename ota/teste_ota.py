import requests
#from requests.auth import HTTPBasicAuth
import json

def open_json_ota():
    with open('vars_1.json', 'r') as rj:
        survey_data = json.load(rj)
    rj.close()
    return survey_data

survey_data = open_json_ota()
login = survey_data["login_site"]
senha = survey_data["senha_site"]
response= requests.get('https://projeto-iot-0722.000webhostapp.com/ota', auth=(login, senha))
print(response)