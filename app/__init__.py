from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mqtt import Mqtt

app = Flask(__name__)


app.config['MQTT_BROKER_URL'] = '172.17.0.2'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
# app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
# app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes



mqtt_client = Mqtt(app)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    print('Connected to MQTT Broker!')

@mqtt_client.on_message()
def on_message(client, userdata, message):
    m =str(message.payload.decode("utf-8"))
    print("message received: "  ,m)
    if m == 'GO':
        print('This is working!')

mqtt_client.subscribe('home/mytopic')

app.secret_key = "nextrad1234"
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)



from app import routes, models

# mqtt.subscribe('home/mytopic')



# # mqtt.conn

