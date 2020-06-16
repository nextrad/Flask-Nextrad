from app import app
from flask import Flask, render_template, request, redirect, url_for, flash
from app.models import Pulse, RadarParameters
from app import db, experiment, mqtt_config, ConManager
import configparser
import json
from flask_mqtt import Mqtt
import time
import ast
import collections

mq_client_name = mqtt_config['DEFAULT']['ClientName']
mq_connections = mqtt_config['Channels']['Connections']
mq_expdict = mqtt_config['Channels']['ExperimentDict']
mq_status = mqtt_config['Channels']['Status']
mq_gpsdos = mqtt_config['Channels']['Gpsdos']

mq_Node0_start = mqtt_config['RunAddresses']['Node0_start']
mq_Node1_start = mqtt_config['RunAddresses']['Node1_start']
mq_Node2_start = mqtt_config['RunAddresses']['Node2_start']

mq_runners={'Node0':mq_Node0_start ,'Node1':mq_Node1_start,'Node2':mq_Node2_start}


try:
    mqtt_client = Mqtt(app)
    mq_is_running = 1

except:
    print('Please Restart with MQTT Broker Running')
    mq_is_running = 0
# mqtt_client.name = mq_client_name

def update(d, u):
    for k, v in u.items():
        if isinstance(d, collections.Mapping):
            if isinstance(v, collections.Mapping):
                r = update(d.get(k, {}), v)
                d[k] = r
            else:
                d[k] = u[k]
        else:
            d = {k: u[k]}
    return d

def update_connections(m):
    # try:
    temp=ast.literal_eval(m)
    ConManager.conman.cond = update(ConManager.conman.cond,temp)
    ConManager.conman.node_valid()


if mq_is_running:
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
        if str(message.topic)[0:12] == mq_gpsdos[0:12]: #Bit of a hack for string checking ..
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


    connection_status_topic = mq_connections[:-2] +'/'+ mq_client_name
    print('Publishing to', connection_status_topic)
    mqtt_client.subscribe(mq_connections)
    print('Mqtt client Connected to',mq_connections)
    mqtt_client.subscribe(mq_expdict)
    mqtt_client.subscribe(mq_status)
    mqtt_client.subscribe(mq_gpsdos)

    temp = {mq_client_name:{mq_client_name:{"name":mq_client_name,"connection":True,"ip":"192.168.100"}}}
    mqtt_client.publish(connection_status_topic,str(temp),0,True)
    for node, v in mq_runners.items():
        mqtt_client.publish(mq_runners[node], str({node:{"Status":{"run":0}}}), 0, False)
