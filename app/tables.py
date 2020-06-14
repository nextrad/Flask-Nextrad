from app import app
from flask import Flask, render_template, request, redirect, url_for, flash
from app.models import Pulse, RadarParameters
from app import db
import configparser
import json
import ast


class PulseDefaults:
    pulse_config = configparser.ConfigParser()
    pulse_config.read('./configs/server_config.ini')

    def __init__(self, pulse_config=pulse_config):
        self.L_frequency = json.loads(pulse_config.get('PulseTableDefaults','L_frequency'))
        self.X_frequency = json.loads(pulse_config.get('PulseTableDefaults','X_frequency'))
        self.L_pols_num = json.loads(pulse_config.get('PulseTableDefaults','L_pols'))
        self.X_pols_num = json.loads(pulse_config.get('PulseTableDefaults','X_pols'))
        self.p_width = json.loads(pulse_config.get('PulseTableDefaults','p_width'))

        self.target_descriptions = ast.literal_eval(pulse_config.get('TargetDescription','targets'))
        self.position_favourites = ast.literal_eval(pulse_config.get('PositionFavourites','position'))
        # print((self.target_descriptions['Drones'][0]))

        self.L_frequency_str = []
        self.X_frequency_str = []
        self.p_width_str = []

        for L in self.L_frequency:
            self.L_frequency_str.append(str(L))
        for X in self.X_frequency:
            self.X_frequency_str.append(str(X))
        for p in self.p_width:
            self.p_width_str.append(str(p))

        self.L_pols_str = []
        self.X_pols_str = []
        for pol in self.L_pols_num:
            if pol == 0:
                self.L_pols_str.append('VV')
            if pol == 1:
                self.L_pols_str.append('VH')
            if pol == 2:
                self.L_pols_str.append('HV')
            if pol == 3:
                self.L_pols_str.append('HH')

        for pol in self.X_pols_num:
            if pol == 4:
                self.X_pols_str.append('V/VH')
            if pol == 5:
                self.X_pols_str.append('H/VH')

        self.defaults={
            'L_frequency':self.L_frequency,
            'X_frequency':self.X_frequency,
            'L_frequency_str':self.L_frequency_str,
            'X_frequency_str':self.X_frequency_str,
            'L_pols_num':self.L_pols_num,
            'X_pols_num':self.X_pols_num,
            'L_pols_str':self.L_pols_str,
            'X_pols_str':self.X_pols_str,
            'p_width':self.p_width,
            'p_width_str':self.p_width_str,

            'posfav':self.position_favourites,
            'tgts':self.target_descriptions
        }

class RadarParams:

    def __init__(self):
        self.pri = db.session.query(RadarParameters).order_by(RadarParameters.id.desc()).first().pri
        self.range_samples = db.session.query(RadarParameters).order_by(RadarParameters.id.desc()).first().range_samples
        self.num_pulse = db.session.query(RadarParameters).order_by(RadarParameters.id.desc()).first().num_pulse


pulse_defaults = PulseDefaults()
radar_params = RadarParams()



@app.route('/updatepp', methods = ['POST'])
def submit_pulse_params():
    if request.method == 'POST':
        radar_params.pri = request.form['pri']
        radar_params.num_pulse = request.form['num_pulse']
        radar_params.range_samples = request.form['range_samples']
        # print(radar_params.pri,radar_params.num_pulse,radar_params.range_samples)

        param = RadarParameters(radar_params.pri,radar_params.num_pulse,radar_params.range_samples)
        db.session.add(param)
        db.session.commit()

        flash("Edited Radar Parameters")
        return redirect(url_for('index'))

#insert data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        frequency = request.form['frequency']
        polarisation = request.form['polarisation']
        pulse_width = request.form['pulse_width']
        pri=radar_params.pri
        pulse = Pulse(frequency, pulse_width, polarisation,pri)
        db.session.add(pulse)
        db.session.commit()
  
        flash("Pulse Added Successfully")
        return redirect(url_for('index'))
  
#update employee
@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        pulse = Pulse.query.get(request.form.get('id'))
  
        pulse.frequency = request.form['frequency']
        pulse.polarisation = request.form['polarisation']
        pulse.pulse_width = request.form['pulse_width']
        pri = radar_params.pri
        db.session.commit()
        flash("Pulse Edited Successfully")
        return redirect(url_for('index'))
  
#delete pulse
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    pulse = Pulse.query.get(id)
    db.session.delete(pulse)
    db.session.commit()
    flash("Pulse Deleted Successfully")
    return redirect(url_for('index'))