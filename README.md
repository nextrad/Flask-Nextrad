# Flask-Nextrad
A flask app for NeXtRAD radar control

To run:
	gunicorn --worker-class gevent --workers 1 --threads 4 --bind 0.0.0.0:5000 app:app 
