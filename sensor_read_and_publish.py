import os
import configparser #https://stackoverflow.com/questions/29344196/creating-a-config-file
from __init__ import SDS011
import time
from datetime import datetime
import json
import paho.mqtt.publish as publish
import sys

basedir = os.path.abspath(os.path.dirname(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(basedir, 'aqm.cfg'))
device_path = config['SDS011']['device_path'] # $ dmesg | grep tty
dictionary = {}
warmup_time = int(config['SDS011']['warmup_time']) # Should be 60 seconds to get qualified values
try:
    print('Initialising...')
    sensor = SDS011(device_path, use_query_mode=True)
    print('Setting report mode...')
    sensor.set_report_mode(read=False, active=False)
    print('Turning on fan and diode in case in sleep mode...')
    sensor.sleep(sleep=False)  # Turn on fan and diode in case in sleep mode
    print('The sensor is warming-up during the next '+str(warmup_time)+' seconds!')
    time.sleep(warmup_time)  # Should be 60 seconds to get qualified values
    while True:
        values = sensor.query()
        if values is not None:
            dictionary = {
                "time" : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "pm2.5" : values[0],
                "pm10" : values[1],
            }
            payload = json.dumps(dictionary, default=str)
            print('MQTT payload (jsonised):\n'+payload)
            publish.single(
                topic=config['MQTT']['topic'], #"aqm/kabul/station02", #"aqm/kabul/station01",
                payload=payload,
                hostname="broker.hivemq.com",
                port=8000,
                client_id=config['MQTT']['client_id'], #"Station_02_Mikrorayan", #"Station_01_OfficeK3",
                transport="websockets",
            )
            print('Published to "'+config['MQTT']['topic']+'"\nSensor now set to sleep mode.')
            sensor.sleep(sleep=True)
            # sensor = SDS011(device_path, use_query_mode=False)
            sensor = None
            print('End of script!')
            break
        else:
            print("No values read! Waiting for 2 seconds and then will try to read again...")
            time.sleep(2)

except KeyboardInterrupt:
    print('\nExiting(and resetting)...') # resetting sensor
    sensor = SDS011(device_path, use_query_mode=False)
    sensor.set_report_mode(read=True, active=True)
    sensor.sleep(sleep=False)  # Turn on fan and diode in case it was in sleep mode
    sensor = None
    sys.exit("Sensor reset due to a KeyboardInterrupt\n")
