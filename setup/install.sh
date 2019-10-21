#!/usr/bin/sh

sed  's|{path}|'${PWD}'|' ./setup/smmqtt.service > /etc/systemd/system/smmqtt.service

FILE=/etc/smmqtt.conf
if test -f "$FILE"; then
    echo "$FILE exist, skipping"
else
    cp ./setup/settings.cfg $FILE
fi
systemctl enable smmqtt.service
systemctl start smmqtt.service

