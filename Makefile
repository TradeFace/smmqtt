init:
	pip3 install -r requirements.txt

install:
	sudo sed  's|{path}|'${PWD}'|' ./setup/smmqtt.service > /etc/systemd/system/smmqtt.service
	sudo cp ./setup/settings.cfg /etc/smmqtt.conf
	sudo systemctl enable smmqtt.service
	sudo systemctl start smmqtt.service

