# Mosquitto setup

MQTT broker

## FS setup

Change folders owner to 1883:1883 (fixed uid:gid from docker image)

`sudo chwon 1883:1883 data`

`sudo chwon 1883:1883 log`


## Password setup

Create file `mosquitto.passwd` in the current folder.
Need to use `mosquitto_passwd` util from mosquitto image to create this file.


First run `docker run -it eclipse-mosquitto /bin/sh` to get interactive shell for mosquitto.
Create a file via `vi` with next format `<username>:<password>`.
Run `mosquitto_passwd -U <filename>` to encode passwords.
Copy results and create `mosquitto.passwd` file with this content on host machine.
Put this file near configuration `mosquitto.conf`
