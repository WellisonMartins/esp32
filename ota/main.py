
from util import create_mqtt_client, get_telemetry_topic, get_c2d_topic, open_json, sensor_get_values, get_telemetry_topic
import utime
import _thread
import json
import gc
import time

import machine

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

#collect from topic
def pub_sub():
    global datadataset_dec_rep_j
    try:
        while True:
            print("Listening")
            mqtt_client.reconnect()
            subscribe_topic = get_c2d_topic(survey_data['device_id'])
            mqtt_client.set_callback(callback_handler)
            mqtt_client.subscribe(topic=subscribe_topic)
            try:          
                data = sensor_get_values()
                topic = get_telemetry_topic(survey_data['device_id'])
                mqtt_client.publish(topic=topic, msg=data)
                print("Telemetria Enviada")
            except: 
                None      
            mqtt_client.check_msg()
            dataset = message_received
            dataset_dec = dataset.decode("utf-8")
            print(dataset_dec)
            utime.sleep(1)
            mqtt_client.disconnect()
    except Exception as e: 
        print("Sub function error: ", e)
        mqtt_client.disconnect()

while True:
    pub_sub()
