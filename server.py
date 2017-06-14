#!/usr/bin/env python3
"""
Poll HUE bridge sensors and raise MQTT events
if a button on a dimmer was pressed
"""

import sys
import time
import os
import qhue
import signal
import paho.mqtt.client as mqtt

__memory__ = {}
__mqttc__ = mqtt.Client()
__mqttc__.connect(os.environ.get('MQTT_BROKER'), 1883)
__mqttc__.loop_start()


def clean_exit(_signo, _stack_frame):
    """
    Close MQTT connections and log
    """
    print("Exiting")
    __mqttc__.loop_stop()
    __mqttc__.disconnect()
    sys.exit(0)
signal.signal(signal.SIGTERM, clean_exit)

def notify(uniqueid, message):
    """
    Notify button state change via MQTT
    """
    __mqttc__.publish(os.environ.get('MQTT_TOPIC', 'dimmers/{}').format(uniqueid),
                      message)

def check_change(sensor):
    """
    Check if button state changed, and call notfy() if so
    Update last-seen-state map
    """
    if sensor['state']['lastupdated'] != __memory__.get(sensor['uniqueid'], False):
        change = sensor['state'].get('buttonevent')
        notify(sensor['uniqueid'], change)
        print("Button {} pushed on {}".format(sensor['uniqueid'], change))
    __memory__[sensor['uniqueid']] = sensor['state']['lastupdated']

def main():
    """
    main
    """
    hue_bridge = qhue.Bridge(os.environ.get('HUE_BRIDGE'),
                             os.environ.get('HUE_USERNAME'))
    if not hue_bridge:
        print("Oops")
        sys.exit(1)
    sensors = hue_bridge.sensors
    for _, sensor in sensors().items():
        if sensor.get('type') == 'ZLLSwitch':
            __memory__[sensor['uniqueid']] = sensor['state']['lastupdated']
    print("Started")
    sleep_time = os.environ.get('SLEEP_TIME', 0.3)
    while True:
        try:
            for _, sensor in sensors().items():
                if sensor.get('type') == 'ZLLSwitch':
                    check_change((sensor))
            time.sleep(sleep_time)
        except KeyboardInterrupt:
            clean_exit(False, False)
            break
main()
