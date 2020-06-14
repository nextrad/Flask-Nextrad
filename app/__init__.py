from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mqtt import Mqtt
import configparser


mqtt_config = configparser.ConfigParser()
mqtt_config.read('./configs/mqtt_config.ini')

app = Flask(__name__)


app.config['MQTT_BROKER_URL'] = mqtt_config['DEFAULT']['BrokerAddr']
app.config['MQTT_BROKER_PORT'] = int(mqtt_config['DEFAULT']['Port'])
app.config['MQTT_KEEPALIVE'] = int(mqtt_config['DEFAULT']['KeepAlive']) # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
app.config['MQTT_CONNECTED_FLAG'] = False
app.config['MQTT_BAD_CONNECTION_FLAG'] = False
app.config['MQTT_RETRY_COUNT'] = 2
app.config['MQTT_CLIENT_NAME'] = 'CNC'


app.secret_key = "nextrad1234"
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

from app import mqttclient