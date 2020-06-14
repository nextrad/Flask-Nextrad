from app import app
from flask import Flask, render_template, request, redirect, url_for, flash
from app.models import Pulse, RadarParameters
from app import db, mqtt_client
import configparser
import json
from app import tables
from flask_mqtt import Mqtt



class Experiment:
    def __init__(self):
        server_config = configparser.ConfigParser()
        server_config.read('./configs/server_config.ini')
        self.radar_config=configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.radar_config.optionxform = lambda option: option
        radar_ini = server_config.get('DEFAULT','radar_config')
        self.radar_config.read(radar_ini)
        # Pulse Params
        self.exp_dict = {}
        self.waveform_index = self.radar_config.get('PulseParameters','WAVEFORM_INDEX')
        self.num_pris = self.radar_config['PulseParameters']['NUM_PRIS']
        self.pre_pulse = self.radar_config['PulseParameters']['PRE_PULSE']
        self.pri_pulse_width = self.radar_config['PulseParameters']['PRI_PULSE_WIDTH']
        self.X_amp_delay = self.radar_config['PulseParameters']['X_AMP_DELAY']
        self.L_amp_delay = self.radar_config['PulseParameters']['L_AMP_DELAY']
        self.rex_delay = self.radar_config['PulseParameters']['REX_DELAY']
        self.dac_delay = self.radar_config['PulseParameters']['DAC_DELAY']
        self.adc_delay = self.radar_config['PulseParameters']['ADC_DELAY']
        self.sample_per_pri = self.radar_config['PulseParameters']['SAMPLES_PER_PRI']
        self.pulses = self.radar_config['PulseParameters']['PULSES']
        # TargetSettings
        self.tgt_lat = self.radar_config['TargetSettings']['TGT_LOCATION_LAT']
        self.tgt_long = self.radar_config['TargetSettings']['TGT_LOCATION_LON']
        self.tgt_description = 'None'

        self.pri = 0.0
        self.update_exp_dict()

    def update_exp_dict(self):
        self.exp_dict = {
            'PulseParams':{
                'waveform_index':self.waveform_index,
                'num_pris':self.num_pris,
                'pre_pulse':self.pre_pulse,
                'pri_pulse_width':self.pri_pulse_width,
                'X_amp_delay':self.X_amp_delay,
                'L_amp_delay':self.L_amp_delay,
                'rex_delay':self.rex_delay,
                'dac_delay':self.dac_delay,
                'adc_delay':self.adc_delay,
                'sample_per_pri':self.sample_per_pri
            },
            'TargetSettings':{
                'tgt_description':self.tgt_description,
                'tgt_lat':self.tgt_lat,
                'tgt_long':self.tgt_long
            }
        }




@app.route('/run', methods = ['POST'])
def run():
    if request.method == 'POST':

        pulses = Pulse.query.all()
        radar_params={'pri':str(tables.radar_params.pri),'num_pulse':str(tables.radar_params.num_pulse),'range_samples':str(tables.radar_params.range_samples)}
        experiment.pri = radar_params['pri']
        experiment.num_pris = radar_params['num_pulse']
        experiment.sample_per_pri = radar_params['range_samples']
        experiment.pulses = format_pulses(pulses)
        experiment.update_exp_dict()

        # print(experiment.exp_dict)

        mqtt_client.publish('home/mytopic', str(experiment.exp_dict))

        flash("Experiment Running")
        return redirect(url_for('index'))

def format_pulses(pulses):
    string = ''
    for pulse in pulses:
        print(pulse)
        if pulse.polarisation == 'VV':
            polarisation = '0'
        if pulse.polarisation == 'VH':
            polarisation = '1'
        if pulse.polarisation == 'HV':
            polarisation = '2'
        if pulse.polarisation == 'HH':
            polarisation = '3'
        if pulse.polarisation == 'V/VH':
            polarisation = '4'
        if pulse.polarisation == 'H/VH':
            polarisation = '5'
        string+='|'+pulse.pulse_width \
            +','+pulse.pri \
            +','+polarisation \
            +','+pulse.frequency
    string = string[1:]
    return string


experiment = Experiment()


