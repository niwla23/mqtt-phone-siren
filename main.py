#!/usr/bin/python
import multiprocessing
from time import sleep
from typing import Optional
from fritzconnection import FritzConnection
import os
import paho.mqtt.client as mqtt


class Config:
    def __init__(self) -> None:
        self.FB_ADDRESS = os.environ["FB_ADDRESS"]
        self.FB_USER = os.environ["FB_USER"]
        self.FB_PASSWORD = os.environ["FB_PASSWORD"]
        self.MQTT_HOST = os.environ["MQTT_HOST"]
        self.MQTT_PORT = int(os.environ["MQTT_PORT"])
        self.MQTT_TOPIC = os.environ["MQTT_TOPIC"]
        self.PHONE_NUMBER = os.environ.get("PHONE_NUMBER") or "**9"


config = Config()

fc = FritzConnection(
    address=config.FB_ADDRESS,
    user=config.FB_USER,
    password=config.FB_PASSWORD,
)

print(fc)
caller_process: Optional[multiprocessing.Process] = None


def alarm_on():
    fc.call_action("X_VoIP1", "X_AVM-DE_DialNumber",
                   arguments={"NewX_AVM-DE_PhoneNumber ": config.PHONE_NUMBER})


def alarm_off():
    fc.call_action("X_VoIP1", "X_AVM-DE_DialHangup")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(config.MQTT_TOPIC)


def on_message(client, userdata, msg):
    payload = msg.payload.decode().upper()
    print("received payload:", payload)
    if payload == "ON":
        alarm_on()
    elif payload == "OFF":
        alarm_off()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(config.MQTT_HOST, config.MQTT_PORT, 60)
client.loop_forever()
