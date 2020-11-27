## Air Quality Monitor - minimum code for Afghanistan

--------------------------------------------------------------------------------

### Activating SSH on Raspberry Pi (headless):

Create an empty file named `ssh` and put it in the root folder of `boot` partition in the microSD, and NOT in the `rootfs` partition.

Can also be activated with `$ sudo raspi-config` if keyboard and display access is available.

--------------------------------------------------------------------------------

### Updating the Raspberry Pi:

##### current mobile traffic is 90MB per day; therefore the divided download

```
sudo apt -y update
sudo apt list --upgradable
sudo apt-mark hold <package_name>
sudo apt -y full-upgrade --download-only
sudo apt-mark unhold <package_name>

< Next Day >
sudo apt -y full-upgrade --download-only
sudo apt -y full-upgrade
```

#### or if the above gets stuck while downloading then try the following:
```
sudo apt -y -o Acquire::ForceIPv4=true update
sudo apt list --upgradable
sudo apt-mark hold raspberrypi-kernel
sudo apt -y -o Acquire::ForceIPv4=true full-upgrade --download-only
sudo apt-mark unhold raspberrypi-kernel

< Next Day >
sudo apt -y -o Acquire::ForceIPv4=true full-upgrade --download-only
sudo apt -y -o Acquire::ForceIPv4=true full-upgrade
```

#### And then reboot:
```
sudo shutdown -r now
sudo reboot now
```

--------------------------------------------------------------------------------

### Setting up the Raspberry Pi for running the python code:

#### To setup Git and clone the repository:
```
sudo apt -y install git
sudo git clone https://github.com/sarkashr/aqm-afg.git
```
Note: run `sudo git pull` from inside the `aqm-afg` directory to sync with the repository.

#### To setup PIP and the required Python packages:
```
sudo apt -y install python3-pip
sudo pip3 install wheel
sudo pip3 install -r /home/pi/aqm-afg/requirements.txt
```

#### Setting up the cron table entries:
```
sudo crontab -e
```
then add the following lines to the crontab file:
```
*/5 * * * * python3 /home/pi/aqm-afg/sensor_read_and_publish.py
```
#### Modify the MQTT topic and client_id in aqm.cfg file accordingly:
```
sudo nano /home/pi/aqm-afg/aqm.cfg
```
#### And then the final reboot to activate the main script:
```
sudo shutdown -r now
sudo reboot now
```

--------------------------------------------------------------------------------

### To check the incomming MQTT payload:
```
http://www.hivemq.com/demos/websocket-client/
Host -> broker.hivemq.com
Port -> 8000
Subscriptions -> Add New Topic Subscription -> <topic_name>
<topic name> example: "aqm/kabul/station09"
```

--------------------------------------------------------------------------------

### Setting up a remoteiot.com new device:
```
sudo apt install openjdk-8-jre-headless
```

In the RemoteIoT Dashboard go to Devices and there choose Register New Device.
After filling the fields, copy the command line code and execute it with `sudo` in the RPi.
Most likely there's already an open SSH session to the RPi for pasting and executing the above copied command.

Note: Java 11, 10 & 9 don't work on Pi Zero because of ARMv6 architecture.

--------------------------------------------------------------------------------
