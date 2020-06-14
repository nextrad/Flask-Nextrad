from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from app.models import Pulse
from app import db, mqtt_client
from app import tables, experiment, mappy
import configparser
import json
import datetime
# from app import mqttclient



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
    mapbox_access_token = 'pk.eyJ1IjoidXNlbmFtZXVzdXJwZXIiLCJhIjoiY2p6ZHdtMG9vMGJrNDNxdWl0OWJuZG9qeiJ9.YfrEsL3WyMm3aPG-kRXz1g'
    return render_template('map.html',mapbox_access_token=mapbox_access_token,lati=lati,longi=longi,defaults=defaults)

