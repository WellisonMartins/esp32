
from robust import MQTTClient
import re #regex para coletar os valores do form
import json
from machine import ADC, Pin, I2C
import machine
import random
from time import sleep
import time
import utime
import esp32

try:
  import usocket as socket
except:
  import socket



#Funcoes para integarir via mqtt com o iothub
def create_mqtt_client(client_id, hostname, username, password, port=8883, keepalive=60, ssl=True):
    if not keepalive:
        keepalive = 60
    if not ssl:
        ssl = True
    c = MQTTClient(client_id=client_id, server=hostname, port=8883, user=username, password=password, keepalive=60, ssl=True)
    c.DEBUG = True
    return c

def get_telemetry_topic(device_id):
    return get_topic_base(device_id) + "/messages/events/"

    

def get_c2d_topic(device_id):
     return get_topic_base(device_id) + "/messages/devicebound/#"



def get_topic_base(device_id, module_id=None):
    if module_id:
        base_str = "devices/" + device_id + "/modules/" + module_id
    else:
        base_str = "devices/" + device_id
    return base_str

DELIMITER = ";"
VALUE_SEPARATOR = "="

def parse_connection(connection_string):
    cs_args = connection_string.split(DELIMITER)
    dictionary = dict(arg.split(VALUE_SEPARATOR, 1) for arg in cs_args)
    return dictionary

def save_json(dictValues):
    with open('vars.json', 'w') as sj: 
        json.dump(dictValues, sj)
    sj.close()
    print("Arquivo salvo!. Reiniciando")
    sleep(1)
    reset()



def open_json():
    with open('vars.json', 'r') as rj:
        survey_data = json.load(rj)
        survey_data['sas_token_str'] = survey_data['sas_token_str'].replace(" ","_")
    rj.close()
    return survey_data

##############################################
#Projeto com Sensor de Movimento
#Sensor Wellison

movement_sensor = Pin(4, Pin.IN, Pin.PULL_UP)
led = Pin(2, Pin.OUT)

def sensor_get_values():
  if movement_sensor.value() == 0: 
    None
  else:
    movement_value = "Motion captured"
    led.value(1)
    time.sleep(0.5)
    sleep(0.5)

  temp = esp32.raw_temperature()
  tempC = (temp - 32) / 1.8

  msg = {}
  msg["Movement_Sensor"] = movement_value
  msg["Temperatura_interna_da_ESP"] = tempC

  return json.dumps(msg)
