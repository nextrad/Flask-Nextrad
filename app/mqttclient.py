from app import app
from flask import Flask, render_template, request, redirect, url_for, flash
from app.models import Pulse, RadarParameters
from app import db, experiment, mqtt_config, ConManager
import configparser
import json
from flask_mqtt import Mqtt
import time
import ast

mq_client_name = mqtt_config['DEFAULT']['ClientName']
mq_connections = mqtt_config['Channels']['Connections']
mq_expdict = mqtt_config['Channels']['ExperimentDict']
mq_status = mqtt_config['Channels']['Status']

mqtt_client = Mqtt(app)
# mqtt_client.name = mq_client_name

connection_status_topic = mq_connections[:-2] +'/'+ mq_client_name
print('Publishing to', connection_status_topic)

def update_connections(m):
    # try:
    temp=ast.literal_eval(m)
    ConManager.conman.cond.update(temp)

    return redirect(url_for('connection'))
    # except:
    #     print('Please check format of MQTT string!')

    # print(ConManager.conman.cond)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    print('Connected to MQTT Broker!')
    if rc==0:
        # print("Client Connected:",cli)
        print("connected OK Returned code=",rc)
        print("Client Connected:",client.name)
        client.connected_flag=True #Flag to indicate success
    else:
        print("Bad connection Returned code=",rc)
        client.bad_connection_flag=True

@mqtt_client.on_message()
def on_message(client, userdata, message):
    m =str(message.payload.decode("utf-8"))
    if str(message.topic)[0:12] == mq_connections[0:12]: #Bit of a hack for string checking ..
        update_connections(m)
    if message.topic == 'Radar/Connections' and m == 'GO':
        print('This is working!')

def on_disconnect(client, userdata, flags, rc=0):
    m=client.name+"DisConnected flags"+"result code "+str(rc)
    print(m)
    client.connected_flag=False
    connection = {client.name:client.connected_flag}
    ConManager.conman.cond.update(connection)

def on_log(client, userdata, level, buf):
    print("log: ",buf)


mqtt_client.subscribe(mq_connections)
print('Mqtt client Connected to',mq_connections)
mqtt_client.subscribe(mq_expdict)
mqtt_client.subscribe(mq_status)

temp = {mq_client_name:{"name":mq_client_name,"connected":True}}
mqtt_client.publish(connection_status_topic,str(temp),0,True)


# mqtt_client.will_set(connection_status_topic,str({mq_client_name:{"name":mq_client_name,"connected":False}}),0,True) #set will message


# mq_connection_status_topic = mq_connections + mq_client_name

# mqtt_client.will_set(mq_connection_status_topic,"False",0,True)
