from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify, make_response
from app.models import Pulse
from app import db
from app import tables, experiment, mappy, ConManager
import configparser
import json
import datetime
from importlib import import_module
import os
from flask import Flask, render_template, Response
from datetime import datetime
from functools import wraps, update_wrapper
import cv2
import numpy as np

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)

def connect_cameras():
    try:
        Camera0 = import_module('camera_opencv').Camera
        # Camera0.set_video_source(0)
        cam0=1
    except RuntimeError:
        Camera0 = None
        cam0=0
    try:
        Camera1 = import_module('camera_opencv').Camera1
        # Camera1.set_video_source(1)
        # Camera1 = None
        cam1=1
    except RuntimeError:
        Camera1 = None
        cam1=0
    try:
        # Camera2 = import_module('camera_v4l2').Camera
        # Camera2.set_video_source(2)
        Camera2 = None
        cam2=0
    except RuntimeError:
        Camera2 = None
        cam2=0

    return cam0,cam1,cam2, Camera0, Camera1,Camera2

cam0, cam1, cam2, Camera0, Camera1, Camera2 = connect_cameras()

nc_image = 'static/no_con.jpg'

@app.route('/',methods=['GET','POST'])
@app.route('/control',methods=['GET','POST'])
def index():
    pulses = Pulse.query.all()
    defaults=tables.pulse_defaults.defaults
    radar_params={'pri':str(tables.radar_params.pri),'num_pulse':str(tables.radar_params.num_pulse),'range_samples':str(tables.radar_params.range_samples)}
    return render_template('control.html', title='Control',pulses=pulses,defaults=defaults,radar_params=radar_params)


@app.route('/video',methods=['GET','POST'])
def video():
    con = {'Cam0':cam0,'Cam1':cam1,'Cam2':cam2}
    return render_template('video.html',image=nc_image,con=con)


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

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed_0')
def video_feed_0():
    """Video streaming route. Put this in the src attribute of an img tag."""
    if cam0==1:
        return Response(gen(Camera0()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_1')
def video_feed_1():
    """Video streaming route. Put this in the src attribute of an img tag."""
    if cam1 == 1:
        return Response(gen(Camera1()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_2')
def video_feed_2():
    """Video streaming route. Put this in the src attribute of an img tag."""
    if cam2==1:
        return Response(gen(Camera2()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/testpage2')
def suggestions():
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    jtime = {'time':time}
    return render_template('testpage2.html', time=time)

# @nocache
@app.route('/connections')
def connection():
    ConManager.send_message(ConManager.conman.cond)
    # toggles = []
    # for node, value in ConManager.conman.cond.items():
    for node in ConManager.conman.cond:
        if node != 'CNC':
            print(node,ConManager.conman.cond[node]['Include'])
    return render_template('connections.html', server_ip='10.0.0.111:5000')
