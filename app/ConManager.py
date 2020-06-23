from app import app
from app import mqttclient, mqtt_config, db
import configparser
import ast
import yaml
import ruamel.yaml
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, send
import collections

clients = []

socketio = SocketIO(app)

def update_dict(d, u):
    for k, v in u.items():
        if isinstance(d, collections.Mapping):
            if isinstance(v, collections.Mapping):
                r = update_dict(d.get(k, {}), v)
                d[k] = r
            else:
                d[k] = u[k]
        else:
            d = {k: u[k]}
    return d

def node_toggles(msg):
    conman.cond=update_dict(conman.cond,msg)


@socketio.on('message')
def handleMessage(msg):
    print('Message: ', msg)
    # send(msg,json=True,broadcast=True)
    try:
        x = ast.literal_eval(msg)
        node_toggles(x)
        # socketio.send(conman.cond)
    except:
        print('Print Not a Dictionary')
        pass

@socketio.on('connect')
def handle_connect():
    # print('Client connected')
    clients.append(request.sid)
    socketio.send(conman.cond)

@socketio.on('disconnect')
def handle_disconnect():
    # print('Client disconnected')
    clients.remove(request.sid)

def send_message(data):
    socketio.send(data)

class Connections():

    def __init__(self):
        in_file = './configs/connections.yaml'
        yaml = ruamel.yaml.YAML(typ='safe')

        with open(in_file) as fpi:
            self.cond = yaml.load(fpi)


    def Check_Connections(self):
        print('Connections')

    def node_valid(self):
        for n, values in self.cond.items():
            # for node, v
            if n == 'Node0':
                if values['Node0']['connection'] and values['Rhino0']['connection']and values['Pentek0']['connection']:
                    self.cond=update_dict(self.cond,{'Node0':{'Valid':'medium'}})
                    if values['Cam0']['connection']:
                        self.cond=update_dict(self.cond,{'Node0':{'Valid':'full'}})
            if n == 'Node1':
                if values['Node1']['connection'] and values['Rhino1']['connection']and values['Pentek1']['connection']:
                    self.cond=update_dict(self.cond,{'Node1':{'Valid':'medium'}})
                    if values['Cam1']['connection']:
                        self.cond=update_dict(self.cond,{'Node1':{'Valid':'full'}})
            if n== 'Node2':
                if values['Node2']['connection'] and values['Rhino2']['connection']and values['Pentek2']['connection']:
                    self.cond=update_dict(self.cond,{'Node2':{'Valid':'medium'}})
                    if values['Cam2']['connection']:
                        self.cond=update_dict(self.cond,{'Node2':{'Valid':'full'}})

@app.route('/includenode', methods=['POST'])
def includenode():
    if request.method == 'POST':
        # try:
        node = request.form['cb']
        print(node)
        # state = node.value
        previous_state=conman.cond[node]['Include']
        if previous_state == 'True':
            conman.cond=update_dict(conman.cond,{node:{'Include':'False'}})
        else:
            conman.cond=update_dict(conman.cond,{node:{'Include':'True'}})

    return redirect(url_for('connection'))

conman = Connections()
print(conman.cond)