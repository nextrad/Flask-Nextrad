# from app import app
# from flask import Flask, render_template, request, redirect, url_for, flash
# from app.models import Pulse, RadarParameters
# from app import db, experiment
# import configparser
# import json

# import time


# # def start_mqtt(self):
# #     if self.running == 0:
# # self.running = 1
# # client_name=self.client_name
# # broker=self.broker
# # topic=self.topic_experiment

# print('Joining MQTT Server ...')

# connection_status_topic="/connections/"+client_name

# def on_disconnect(client, userdata, flags, rc=0):
#     m="DisConnected flags"+"result code "+str(rc)
#     print(m)
#     client.connected_flag=False
# def on_connect(client, userdata, flags, rc):
#     if rc==0:
#         print("connected OK Returned code=",rc)
#         client.connected_flag=True #Flag to indicate success
#     else:
#         print("Bad connection Returned code=",rc)
#         client.bad_connection_flag=True
# def on_log(client, userdata, level, buf):
#     print("log: ",buf)
# def on_message(client, userdata, message):
#     print("message received: "  ,str(message.payload.decode("utf-8")))


# mqtt.Client.connected_flag=False #create flags
# mqtt.Client.bad_connection_flag=False #
# mqtt.Client.retry_count=0 #
# # broker = '172.17.0.2'

# client = mqtt.Client(client_name)
# client.on_connect = on_connect
# client.on_disconnect = on_disconnect
# client.on_message = on_message

# print("Publising on ",connection_status_topic )
# print("Setting will message")
# client.will_set(connection_status_topic,"False",0,True) #set will message

# print('Connecting to Broker')
# client.connect(broker)
# print('Subscribing to Topic',topic)
# client.subscribe(topic)

# client.publish(connection_status_topic,"True",0,True)#use retain flag

# try:
#     while True:
#         while not client.connected_flag:
#             client.loop()
#             time.sleep(1)#wait for connection
#             client.loop_start()
#         time.sleep(1)

# except KeyboardInterrupt:
#     print('Exiting')
#     client.publish(connection_status_topic,"False",0,True)
#     client.disconnect()
#     client.loop_stop()

# # mqttclient = MqttClient()
# # mqttclient.start_mqtt()