from app import mqttclient, mqtt_config
import configparser
import ast


class Connections():
    def __init__(self):
        self.CNC=ast.literal_eval(mqtt_config['ExpectedClients']['CNC'])
        self.Node0=ast.literal_eval(mqtt_config['ExpectedClients']['Node0'])
        self.Node1=ast.literal_eval(mqtt_config['ExpectedClients']['Node1'])

        self.cond={}

        self.cond.update(self.CNC)
        self.cond.update(self.Node0)
        self.cond.update(self.Node1)

    def Check_Connections(self):
        print('Connections')

conman = Connections()