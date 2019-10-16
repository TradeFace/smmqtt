init:
	pip3 install -r requirements.txt

install:
	echo "Installing service."
	sudo sed  's|{path}|'${PWD}'|' ./setup/smmqtt.service /etc/systemd/system/smmqtt.service
	sudo systemctl enable smmqtt.service
	sudo systemctl start smmqtt.service
	echo "Done."