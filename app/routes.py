from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
from app.models import Pulse
from app import db
from app import tables, experiment, mappy, ConManager
import configparser
import json
import datetime

@app.route('/',methods=['GET','POST'])
@app.route('/control',methods=['GET','POST'])
def index():
    pulses = Pulse.query.all()
    defaults=tables.pulse_defaults.defaults
    radar_params={'pri':str(tables.radar_params.pri),'num_pulse':str(tables.radar_params.num_pulse),'range_samples':str(tables.radar_params.range_samples)}
    # users = [{'name':'Bob','surname':'Man','handle':'@this','order':'1'},{'name':'Susan','surname':'Fish','handle':'@meep','order':'2'}]
    return render_template('control.html', title='Control',pulses=pulses,defaults=defaults,radar_params=radar_params)


@app.route('/edit')
def test_edit_table():
    pulses = Pulse.query.all()
    defaults=tables.pulse_defaults.defaults
    return render_template('control.html',pulses=pulses,defaults=defaults)

@app.route('/map')
def map():
    lati = experiment.experiment.tgt_lat
    longi = experiment.experiment.tgt_long
    defaults=tables.pulse_defaults.defaults
    target= experiment.experiment.tgt_description
    mapbox_access_token = 'pk.eyJ1IjoidXNlbmFtZXVzdXJwZXIiLCJhIjoiY2p6ZHdtMG9vMGJrNDNxdWl0OWJuZG9qeiJ9.YfrEsL3WyMm3aPG-kRXz1g'
    return render_template('map.html',mapbox_access_token=mapbox_access_token,lati=lati,longi=longi,defaults=defaults,target=target)

@app.route('/connections')
def connection():
    connections = ConManager.conman.cond
    valid_nodes = ConManager.conman.valid_nodes
    include_nodes = ConManager.conman.include_node
    return render_template('connections.html',connections=connections,valid_nodes=valid_nodes,include_nodes=include_nodes)


@app.route('/_stuff', methods= ['GET'])
def stuff():
    print('Working')
    data = ConManager.conman.cond
    # connections = ConManager.conman.cond
    return jsonify(data)


@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(str(message))
    return dict(mdebug=print_in_console)