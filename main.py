
import sys
import configparser

from smmqtt import SmartMeterMQTT

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.cfg')

    server = SmartMeterMQTT(config)
 
    try:
        server.main_loop()
    except KeyboardInterrupt:
        print ("Ctrl C - Stopping server")
        sys.exit(1)
