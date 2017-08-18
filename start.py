#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import os
import time
import signal

# Default configuration
config = {
    'mqtt': {
        'broker': os.getenv('MQTT_BROKER', 'localhost'),
        'port': int(os.getenv('MQTT_PORT', '1883')),
        'prefix': os.getenv('MQTT_PREFIX', 'media'),
        'topic': os.getenv('MQTT_TOPIC', 'led'),
        'user': os.environ.get('MQTT_USER'),
        'password': os.environ.get('MQTT_PASSWORD'),
    },
    'led': {
        'channel': int(os.getenv('LED_CHANNEL', '18')),
        'pwm_cycle': float(os.getenv('LED_PWM_CYCLE', '0.005')),
        'num_flashes' : int(os.getenv('LED_NUM_FLASHES', 3))
    }
}

def mqtt_on_connect(client, userdata, flags, rc):
    """@type client: paho.mqtt.client """

    print("Connection returned result: "+str(rc))

    client.subscribe(config['mqtt']['prefix'] + "/" + config['mqtt']['topic'])
    print("Subscribing to: " + config['mqtt']['prefix'] + "/" + config['mqtt']['topic'])

def mqtt_on_message(client, userdata, message):
    """@type client: paho.mqtt.client """

    try:
        # Decode topic
        cmd = message.topic.replace(config['mqtt']['prefix'], '').strip('/')
        print("Command received: %s (%s)" % (cmd, message.payload))
        flash()
        #action = message.payload.decode()

    except Exception as e:
        print("Error during processing of message: ", message.topic, message.payload, str(e))

def cleanup():
    print("cleanup")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    GPIO.cleanup(config['led']['channel'])

def flash():
    for flashes in range(0, config['led']['num_flashes']):
        for i in range(0,101):      # 101 because it stops when it finishes 100
            pwm.ChangeDutyCycle(i)
            time.sleep(config['led']['pwm_cycle'])
        for i in range(100,-1,-1):      # from 100 to zero in steps of -1
            pwm.ChangeDutyCycle(i)
            time.sleep(config['led']['pwm_cycle'])

try:

    ### Setup MQTT ###
    print("Initialising MQTT...")
    mqtt_client = mqtt.Client(config['mqtt']['prefix'] + "-button-mqtt")
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_message = mqtt_on_message
    if config['mqtt']['user']:
        mqtt_client.username_pw_set(config['mqtt']['user'], password=config['mqtt']['password']);
    mqtt_client.connect_async(config['mqtt']['broker'], config['mqtt']['port'], 60)
    mqtt_client.loop_start()

    ### Setup GPIO ###
    print("Initializing GPIO...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config['led']['channel'], GPIO.OUT)
    pwm = GPIO.PWM(config['led']['channel'], 100)
    pwm.start(0)

    print("Starting main loop...")
    mqtt_client.loop_forever(retry_first_connection=True)
finally:
    cleanup()
