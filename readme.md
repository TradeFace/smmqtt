Smart Meter MQTT
==============

Reads Landis + Gyr E350 (ZCF110) DSMR 4.2 with a cheap usb to tll module and sends the data to MQTT.

Module used:
USB CP2102 to TTL RS232 USB TTL to RS485 Mutual Convert 6 in 1 Convert Module
https://www.aliexpress.com/item/32828039395.html

Fysical connection
------
```
module | RJ11 | RJ12
--------------------
  +5v  |   1  |   2
  GND  |   2  |   3
  RXD  |   4  |   5
```

MQTT
-------
=> state topics now only hold the value. 
other data available via topic/attr
```
smartmeter/1.0.0/state {"value": <meter_id>}
smartmeter/96.1.1/state {"value": <meter_serialnumber>}
smartmeter/1.8.1/state {"value": 4006.282, "unit": "kWh"}
smartmeter/1.8.2/state {"value": 2020.298, "unit": "kWh"}
smartmeter/2.8.1/state {"value": 1393.497, "unit": "kWh"}
smartmeter/2.8.2/state {"value": 3179.669, "unit": "kWh"}
smartmeter/96.14.0/state {"value": 2}
smartmeter/1.7.0/state {"value": 0.138, "unit": "kW"}
smartmeter/2.7.0/state {"value": 0.0, "unit": "kW"}
smartmeter/96.7.21/state {"value": 4}
smartmeter/96.7.9/state {"value": 3}
smartmeter/99.97.0/state {"value": 3}
smartmeter/32.32.0/state {"value": 0}
smartmeter/32.36.0/state {"value": 0}
smartmeter/96.13.1/state 
smartmeter/96.13.0/state 
smartmeter/31.7.0/state {"value": 1}
smartmeter/21.7.0/state {"value": 0.138, "unit": "kW"}
smartmeter/22.7.0/state {"value": 0.0, "unit": "kW"}
smartmeter/24.1.0/state {"value": 3}
smartmeter/96.1.0/state {"value": <gasmeter_serialnumber>}
smartmeter/24.2.1/state {"value": 1642.657, "unit": "m3"}
```

Issues
---------
- meter_id trailing chars are trimmed in regex
- readme MQTT; incorrect reflection output


Useful links
------------
- https://github.com/TradeFace/haconfig/blob/master/packages/smartmeter.yaml
- http://domoticx.com/p1-poort-slimme-meter-hardware/
- https://gejanssen.com/howto/Slimme-meter-uitlezen/index.html
