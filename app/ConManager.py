from app import app
from app import mqttclient, mqtt_config
import configparser
import ast
import yaml
import ruamel.yaml
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, send

clients = []

socketio = SocketIO(app)

def node_toggles(msg):
    conman.include_node.update(msg)
    print(conman.include_node)

@socketio.on('message')
def handleMessage(msg):
    print('Message: ', msg)
    # send(msg,json=True,broadcast=True)
    try:
        x = ast.literal_eval(msg)
        node_toggles(x)
    except:
        print('Print Not a Dictionary')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    clients.append(request.sid)
    socketio.send(conman.cond)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    clients.remove(request.sid)

def send_message(data):
    socketio.send(data)


class Connections():

    def __init__(self):
        in_file = './configs/connections.yaml'
        yaml = ruamel.yaml.YAML(typ='safe')

        with open(in_file) as fpi:
            self.cond = yaml.load(fpi)

        # self.Node_CNC = self.cond['CNC']
        # self.Node_N0 = self.cond['N0']
        # self.Node_N1 = self.cond['N1']
        # self.Node_N2 = self.cond['N2']

        self.valid_nodes={'Node0':'No','Node1':'No','Node2':'No'}
        self.include_node ={'Node0':'True','Node1':'True','Node2':'True'}
        self.node_valid()

    def Check_Connections(self):
        print('Connections')

    def node_valid(self):
        for n, values in self.cond.items():
            # for node, v
            if n == 'Node0':
                if values['Node0']['connection'] and values['Rhino0']['connection']and values['Pentek0']['connection']:
                    self.valid_nodes.update({'Node0':'medium'})
                    if values['Cam0']['connection']:
                        self.valid_nodes.update({'Node0':'full'})
            if n == 'Node1':
                if values['Node1']['connection'] and values['Rhino1']['connection']and values['Pentek1']['connection']:
                    self.valid_nodes.update({'Node1':'medium'})
                    if values['Cam1']['connection']:
                        self.valid_nodes.update({'Node1':'full'})
            if n== 'Node2':
                if values['Node2']['connection'] and values['Rhino2']['connection']and values['Pentek2']['connection']:
                    self.valid_nodes.update({'Node2':'medium'})
                    if values['Cam2']['connection']:
                        self.valid_nodes.update({'Node2':'full'})

@app.route('/includenode', methods=['POST'])
def includenode():
    if request.method == 'POST':
        # try:
        node = request.form['cb']
        print(node)
        # state = node.value
        previous_state=conman.include_node[node]
        if previous_state == 'True':
            conman.include_node.update({node:'False'})
            print(conman.include_node)
        else:
            conman.include_node.update({node:'True'})
            print(conman.include_node)

    return redirect(url_for('connection'))

conman = Connections()
print(conman.cond)