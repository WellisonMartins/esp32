import requests
from requests.auth import HTTPBasicAuth
import json

def open_json():
    with open('vars1.json', 'r') as rj:
        survey_data = json.load(rj)
        #survey_data['sas_token_str'] = survey_data['sas_token_str'].replace(" ","_")
    rj.close()
    return survey_data

survey_data = open_json()
login = survey_data["login_site"]
senha = survey_data["senha_site"]
response= requests.get('https://projeto-iot-0722.000webhostapp.com/ota', auth=HTTPBasicAuth(login, senha))
print(response)
