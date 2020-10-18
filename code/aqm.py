# ********************** START OF RESET SECTION *******************************
import __init__
import time

print('initialising...')
sensor = __init__.SDS011("/dev/ttyUSB0", use_query_mode=False)
print('trying to set mode...')
sensor.set_report_mode(read=True, active=True)
# sensor.sleep()  # Turn off fan and diode
# print('set to sleep mode for 15 seconds')
# time.sleep(15)
print('trying to wake up... (in case in sleep mode)')
sensor.sleep(sleep=False)  # Turn on fan and diode in case it was in sleep mode
print('waiting for 15 seconds...')
time.sleep(15)  # Allow time for the sensor to measure properly
print('a test query -> ' + str(sensor.query()))
print('resetting mode...')
sensor.set_report_mode(read=True, active=True)
print('end of reset script')
sensor = None
# *********************** END OF RESET SECTION ********************************

# ***************************** MAIN CODE *************************************
from sds011 import SDS011
# import time
from datetime import datetime
import json
import paho.mqtt.publish as publish
import sys
import configparser #https://stackoverflow.com/questions/29344196/creating-a-config-file
import os

def printValues(timing, values, unit_of_measure):
    if unit_of_measure == SDS011.UnitsOfMeasure.MassConcentrationEuropean:
        unit = 'µg/m³'
    else:
        unit = 'pcs/0.01cft'
    print("Waited %d secs\nValues measured in %s:    PM2.5  " %
          (timing, unit), values[1], ", PM10 ", values[0])

basedir = os.path.abspath(os.path.dirname(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(basedir, 'aqm.cfg'))
device_path = config['SDS011']['device_path'] # $ dmesg | grep tty
timeout = 9                         # timeout on serial line read
unit_of_measure = SDS011.UnitsOfMeasure.MassConcentrationEuropean
print('\n\n')
print('PRE __init__')
sensor = SDS011(device_path, timeout=timeout, unit_of_measure=unit_of_measure)
print('POST __init__')
print(sensor.workstate)
print(sensor.reportmode)
print("\n\n")
dictionary = {}
try:
    while True:
        sensor.reset() # reset is a safer option than just setting the workstate
        # sensor.workstate = SDS011.WorkStates.Measuring
        print('The sensor needs to warm up for 30 seconds!') # 60 seconds!')
        time.sleep(30)  # Should be 60 seconds to get qualified values. The sensor needs to warm up!
        # sensor.dutycycle = 5  # valid values between 0 and 30
        last = time.time()
        while True:
            last1 = time.time()
            values = sensor.get_values()
            ts = datetime.now()
            if values is not None:
                printValues(time.time() - last, values, sensor.unit_of_measure)
                dictionary = {
                    "time" : '{:%y-%m-%d %H:%M %S}'.format(ts), # with seconds
                    # "time" : '{:%y-%m-%d %H:%M}'.format(ts), # without seconds
                    "pm2.5" : values[1],
                    "pm10" : values[0],
                }
                break
            print("Waited %d seconds, no values read, wait 2 seconds, and try to read again" % (
                time.time() - last1))
            time.sleep(2)

        payload = json.dumps(dictionary, default=str)
        print('MQTT payload (jsonised)-> '+payload+"\n\n")
        publish.single(
            topic=config['MQTT']['topic'], #"aqm/kabul/station02", #"aqm/kabul/station01",
            payload=payload,
            hostname="broker.hivemq.com",
            port=8000,
            client_id=config['MQTT']['client_id'], #"Station_02_Mikrorayan", #"Station_01_OfficeK3",
            transport="websockets",
        )
        print("Read was succesfull. Going to sleep for the next 270 seconds.")
        sensor.workstate = SDS011.WorkStates.Sleeping
        time.sleep(270)
except KeyboardInterrupt:
    sensor.reset()
    sensor = None
    sys.exit("\nSensor reset due to a KeyboardInterrupt\n")
# except:
#     sensor.reset()
#     sensor = None
#     sys.exit("\nSensor reset due to some unknown Error; Please investigate the cause!\n")
