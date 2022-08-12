
from util import create_mqtt_client, get_telemetry_topic, get_c2d_topic, open_json, sensor_get_values, get_telemetry_topic, open_json_ota
import utime
import _thread
import json
import gc
import time
import machine

try: import urequests as requests
except: import requests

gc.collect()
gc.enable()


survey_data = open_json()
username = survey_data['hostname'] + '/' + survey_data['device_id']
### Create UMQTT ROBUST or UMQTT SIMPLE CLIENT
mqtt_client = create_mqtt_client(client_id=survey_data['device_id'], hostname=survey_data['hostname'], username=username, password=survey_data['sas_token_str'].replace("_"," "), port=8883, keepalive=60, ssl=True)


def callback_handler(topic, message_receive):
    global message_received
    message_received = message_receive
    #print("Received message")
    #print(message_receive)
 
def reset_mac():
  print("Reiniciando a pedido")
  machine.reset()
  
def res():
  time.sleep(900)
  print("Reiniciando recorrente")
  machine.reset()

def pub_sub():
    global datadataset_dec_rep_j
    try:
        while True:
            print("Listening - v1.4", str(localtime()))
            mqtt_client.reconnect()
            subscribe_topic = get_c2d_topic(survey_data['device_id'])
            mqtt_client.set_callback(callback_handler)
            mqtt_client.subscribe(topic=subscribe_topic)
            if True:
                mqtt_client.wait_msg()
                #mqtt_client.check_msg()
                dataset = message_received
                dataset_dec = dataset.decode("utf-8")
                dataset_dec_rep = dataset_dec.replace("'","\"")
                datadataset_dec_rep_j = set = json.loads(dataset_dec_rep)
                try:
                    if datadataset_dec_rep_j['act'] == 'main.py': 
                        ota('main.py')
                        print("ooooo")
                        reset_mac()
                    if datadataset_dec_rep_j['act'] == 'util.py': 
                        ota('util.py')
                        print("teste1234")
                        reset_mac()
                    if datadataset_dec_rep_j['act'] == 'vars.json': 
                        ota('vars.json')
                        reset_mac()
                    if datadataset_dec_rep_j['act'] == 'boot.py': 
                        ota('boot.py')
                        reset_mac()                 
                    elif datadataset_dec_rep_j['act'] == "reset": reset_mac()
                    else: print("")
                except: 
                    print("erro - payload enviado: ",datadataset_dec_rep_j)
            else:
                sleep(1)
            mqtt_client.disconnect()
    except Exception as e: 
        print("Sub function error: ", e)
        mqtt_client.disconnect()

def ota(filename):
    survey_data = open_json_ota()
    login = survey_data["login_site"]
    senha = survey_data["senha_site"]
    response= requests.get('https://projeto-iot-0722.000webhostapp.com/ota' + filename, auth=(login, senha))
    x = response.text.find("FAIL")
    x = response.text
    f = open(filename,"w")
    f.write(x)
    f.flush()
    f.close
    print("teste")
    sleep(5)


while True:
    pub_sub()
