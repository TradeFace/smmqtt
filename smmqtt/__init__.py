import time
import sys
import serial
import paho.mqtt.client as mqtt

class SmartMeterMQTT:

    delay = 1
    config = []

    def __init__(self, config):

        self.config = config
        self.serial = serial.Serial()
        self.serial.baudrate = int(config['Serial']['baudrate'])
        self.serial.bytesize = int(config['Serial']['bytesize'])
        self.serial.parity = config['Serial']['parity']
        self.serial.stopbits = int(config['Serial']['stopbits'])
        self.serial.xonxoff = 0
        self.serial.rtscts = 0
        self.serial.timeout = 1
        self.serial.port = config['Serial']['port']
        
        try:
            self.serial.open()
        except:
            sys.exit ("Couldn't open %s. "  % self.serial.name)  

        self.mqtt_topic = "smartmeter"
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.enable_logger()
        self.mqtt_client.username_pw_set(config['MQTT']['user'], config['MQTT']['pass'])
        self.mqtt_client.connect(config['MQTT']['host'], int(config['MQTT']['port']), 60)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.loop_start()   


    def main_loop(self):

        while True:
            #read meter
            print("read")
            response = self.serial.readlines()
            if response:
                self.on_recv()
            time.sleep(self.delay)


    def on_recv(self):
        # process data
        print('on_recv')
        # publish to mqtt
        # self.mqtt_client.publish(("%s/%d/state" % (self.mqtt_topic, ?), value)


    def connack_string(self, state):

        states = [
            'Connection successful',
            'Connection refused - incorrect protocol version',
            'Connection refused - invalid client identifier',
            'Connection refused - server unavailable',
            'Connection refused - bad username or password',
            'Connection refused - not authorised'
        ]
        return states[state]


    def on_connect(self, client, userdata, flags, rc):

        print("MQTT Connection state: %s" % self.connack_string(rc))
        client.subscribe("$SYS/#")