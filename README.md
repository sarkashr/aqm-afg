# aqm-afg

--------------------------------------------------------------------------------

Activating SSH on Raspberry Pi:

Create an empty file named "ssh" and put in the root folder of "boot" partition in the microSD, and NOT in the "rootfs" partition.

--------------------------------------------------------------------------------

Setting up the Raspberry Pi for running the python code:
```
sudo apt -y update
sudo apt -y full-upgrade
```
or if the above gets stuck then try below
```
sudo apt -y -o Acquire::ForceIPv4=true update
sudo apt -y -o Acquire::ForceIPv4=true full-upgrade
```

And then reboot
```
sudo shutdown -r now
```

To setup Git and clone the repository
```
sudo apt -y install git
sudo git clone https://github.com/sarkashr/aqm-afg.git
```
Note: run `sudo git pull` from inside the `aqm-afg` directory to sync with the repository.

```
sudo apt -y install python3-pip
sudo pip3 install wheel
sudo pip3 install -r /home/pi/aqm-afg/code/requirements.txt
```

Setting up the cron table entries:
```
sudo crontab -e
```
then add the following lines to the end of crontab file:
```
@reboot python3 /home/pi/aqm-afg/code/aqm.py &
```
Note: Modify the MQTT topic and client_id in aqm.cfg file accordingly.
```
sudo nano /home/pi/aqm-afg/code/aqm.cfg
```
And then the final reboot
```
sudo shutdown -r now
```

--------------------------------------------------------------------------------

To check the incomming MQTT payload:
```
http://www.hivemq.com/demos/websocket-client/
Host -> broker.hivemq.com
Port -> 8000
Subscriptions -> Add New Topic Subscription -> <topic name>
<topic name> example: "aqm/kabul/station09"
```

--------------------------------------------------------------------------------

Setting up a remoteiot.com new device:
```
sudo apt install openjdk-8-jre-headless
```

In the RemoteIoT Dashboard go to Devices and there choose Register New Device.
After filling the fields, copy the command line code and execute it with `sudo` in the RPi.
Most likely there's already an open SSH session to the RPi for pasting and executing the above copied command.

Note: Java 11, 10 & 9 don't work on Pi Zero because of ARMv6 architecture.

--------------------------------------------------------------------------------
