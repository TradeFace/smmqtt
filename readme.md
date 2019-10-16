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

Useful links
------------
- http://domoticx.com/p1-poort-slimme-meter-hardware/
- https://gejanssen.com/howto/Slimme-meter-uitlezen/index.html