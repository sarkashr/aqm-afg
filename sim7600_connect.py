import os
import time
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(basedir, 'aqm.cfg'))


def bring_sim7600_up():
    getstatus = os.popen('sudo qmicli -d /dev/cdc-wdm0 --dms-get-operating-mode').read().split("\n\t")[1].split("'")[1]
    if getstatus == 'online':
        print("QMI Interface: Geraet ist online")
    else:
        print("QMI Interface: Offline! ...starte Modem")
        startupcommand = 'sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode="online"'
        os.system(startupcommand)
        time.sleep(2)
        getstatus2 = os.popen('sudo qmicli -d /dev/cdc-wdm0 --dms-get-operating-mode').read().split("\n\t")[1].split("'")[1]
        if getstatus2 == 'online':
            print("QMI Interface: Geraet ist nun online")
        else:
            print("QMI Interface: Geraetefehler - konnte nicht aktiviert werden")

def set_raw_ip_mode():
    com0 = 'sudo ip link set wwan0 down'
    com1 = 'echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip'
    com2 = 'sudo ip link set wwan0 up'
    os.system(com0)
    os.system(com1)
    os.system(com2)

def connect_qmi():
    com_connect = 'sudo qmicli -p -d /dev/cdc-wdm0 --device-open-net="net-raw-ip|net-no-qos-header" --wds-start-network='+config['SIM7600']['apn']+' --client-no-release-cid'
    com_dhcp = 'sudo udhcpc -i wwan0'
    os.system(com_connect)
    os.system(com_dhcp)


# if __name__ == "__main__":
bring_sim7600_up()
set_raw_ip_mode()
connect_qmi()
