
from util import create_mqtt_client, get_telemetry_topic, get_c2d_topic, open_json, sensor_get_values, movement_s, get_telemetry_topic, movement_on, movement_off

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
            print("Listening: ")
            mqtt_client.reconnect()
            subscribe_topic = get_c2d_topic(survey_data['device_id'])
            mqtt_client.set_callback(callback_handler)
            mqtt_client.subscribe(topic=subscribe_topic)
            if True:
                mqtt_client.wait_msg()
                dataset = message_received
                dataset_dec = dataset.decode("utf-8")
                dataset_dec_rep = dataset_dec.replace("'","\"")
                datadataset_dec_rep_j = set = json.loads(dataset_dec_rep)
                try:          
                    if datadataset_dec_rep_j['act'] == "reset": reset_mac()              
                    elif datadataset_dec_rep_j['act'] == "keepa": print("keepa")
                    elif datadataset_dec_rep_j['act'] == "getdata": 
                        data = sensor_get_values()
                        topic = get_telemetry_topic(survey_data['device_id'])
                        mqtt_client.publish(topic=topic, msg=data)
                    elif datadataset_dec_rep_j['act'] == "movement_off": 
                        data = movement_off()
                        topic = get_telemetry_topic(survey_data['device_id'])
                        mqtt_client.publish(topic=topic, msg=data)
                    elif datadataset_dec_rep_j['act'] == "movement_on": 
                        data = movement_on()
                        topic = get_telemetry_topic(survey_data['device_id'])
                        mqtt_client.publish(topic=topic, msg=data)
                    elif datadataset_dec_rep_j['act'] == "movement": 
                        data = movement_s()
                    else: print("")
                except: 
                    print("erro - payload enviado: ",datadataset_dec_rep_j)
            else:
                mqtt_client.check_msg()
                utime.sleep(1)
            mqtt_client.disconnect()
    except Exception as e: 
        print("Sub function error: ", e)
        mqtt_client.disconnect()

#while True:
#    sub()
#    utime.sleep(5)
_thread.start_new_thread(movement_s, ())
_thread.start_new_thread(pub_sub, ())
_thread.start_new_thread(res, ())
#_thread.start_new_thread(sub, ())
#web_register_uix()

