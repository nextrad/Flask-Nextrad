from app import app
from flask import Flask, render_template, request, redirect, url_for, flash
from app.models import Pulse, RadarParameters
from app import db, experiment
import configparser
import json

@app.route('/edit_target', methods = ['POST'])
def edit_target():
    if request.method == 'POST':
        experiment.experiment.tgt_lat = request.form['lat']
        experiment.experiment.tgt_long = request.form['long']
        experiment.experiment.tgt_description = request.form['target']
        experiment.experiment.update_exp_dict()
        print(experiment.experiment.tgt_lat,experiment.experiment.tgt_long)
        flash("Target: "+ experiment.experiment.tgt_description +' '+experiment.experiment.tgt_lat+' '+experiment.experiment.tgt_long)
        return redirect(url_for('map'))
