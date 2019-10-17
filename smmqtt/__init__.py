import time
import sys
import serial
import paho.mqtt.client as mqtt
from bitstring import BitArray
import re
import json

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

        data = bytearray()
        line_buffer = []
        while True:
            #read meter
            response = self.serial.readlines()
            #reset the line buffer
            line_buffer = []
            if response:
                c = BitArray(response[0])
                c.invert()
                ba = bytearray.fromhex(c.hex)
                data = bytearray()
                for b in ba:
                    if b == 255:
                        data_decoded = bytes(data).decode('utf-8').strip()
                        line_buffer.append(data_decoded)
                        #reset data
                        data = bytearray()
                        continue
                    data.append((b >> 1))
                self.on_recv(line_buffer)
            time.sleep(self.delay)


    """
    the following 3 functions are not capturing all data
    correctly. But it works good enough for now. 
    """
    def line_cleanup(self, line):

        line = line.replace('LK$','0-1:')
        line = line.replace('T\x02','0-0')
        line = line.replace('T\n','1-0')
        line = line.replace(')\x04',':(')
        line = line.replace('Ca0-1','0-1')
        return line


    def get_value_unit(self, str_data):

        matches = re.split(r'(\d+\.\d+)\*(\w+)', str_data)
        if len(matches) == 1:
            #try int
            matches = re.split(r'(\d+)', str_data)
            if len(matches) == 1:
                return {}
            return {
                'value': int(matches[1])
            }
        return {
            'value': float(matches[1]), 
            'unit_of_measurment': matches[2]
        }

    def get_line_data(self, data_list):

        matches = re.split(r'^([.\d]+)\((.*)\)', data_list)
        data = {'id': matches[0]}
        if len(matches) >= 4:
            data['id'] = matches[1]
            data['string'] = matches[2]
            tmp = self.get_value_unit(matches[2])
            if 'value' in tmp:
                data['parsed'] = tmp
        return data


    def lines_dict(self, lines):

        data = [] 
        for line in lines:
            clean_line = self.line_cleanup(line)
            line_list = clean_line.split(':')
            if len(line_list) < 2:
                continue
            line_data = self.get_line_data(line_list[1])
            data.append(line_data)
        return data

    
    def on_recv(self, lines):
        # process data
        data = self.lines_dict(lines)

        # publish to mqtt
        for item in data:
            value_attr = None
            value = None
            if 'string' in item:
                value_attr = item['string']
                value = item['string']
            if 'parsed' in item:
                value_attr = json.dumps(item['parsed'])
                value = item['parsed']['value']
            #print("%s/%s/state" % (self.mqtt_topic, item['id']), value)
            self.mqtt_client.publish("%s/%s/state" % (self.mqtt_topic, item['id']), value)
            if 'parsed' in item:
                self.mqtt_client.publish("%s/%s/attr" % (self.mqtt_topic, item['id']), value_attr)


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
