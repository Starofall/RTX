from time import sleep

import logging

from colorama import Fore
from flask import json
from paho import mqtt
import paho.mqtt.client as mqtt
from paho.mqtt import subscribe

from rtxlib import info, error, debug, warn, direct_print, inline_print
from rtxlib.dataproviders.DataProvider import DataProvider


class MQTTListenerDataProvider(DataProvider):
    def __init__(self, wf, cp):
        self.callBackFunction = None
        try:
            self.queue = []
            self.host = cp["host"]
            self.port = cp["port"]
            self.topic = cp["topic"]
            self.serializer = cp["serializer"]
            info("> MQTTListener   | " + self.serializer + " | URI: " + self.host + ":" + self.port + " | Topic: " +
                 self.topic, Fore.CYAN)
        except KeyError as e:
            error("mqttListener definition was incomplete: " + str(e))
            exit(1)
        if self.serializer == "JSON":
            self.serialize_function = lambda m: json.loads(m.decode('utf-8'))
        else:
            error("serializer not implemented")
            exit(1)
        try:
            # create mqtt client and connect
            self.mqtt = mqtt.Client()
            self.mqtt.connect(self.host, port=self.port)
            # register callback
            self.mqtt.on_message = self.on_message
            # subscribe and start listing on second thread
            self.mqtt.subscribe(self.topic, 0)
            self.mqtt.loop_start()
        except RuntimeError as e:
            error("connection to mqtt failed: " + str(e))
            exit(1)

    def on_message(self, client, userdata, message):
        # we deserialize each message that comes from mqtt and store it in a queue
        self.queue.append(self.serialize_function(message.payload))

    def reset(self):
        # not used for MQTT, as there is no state to reset
        pass

    def returnData(self):
        try:
            # return the first element in the queue
            return self.queue.pop(0)
        except IndexError:
            return None

    def returnDataListNonBlocking(self):
        # returns the full queue and empties it
        values = self.queue
        self.queue = []
        return values
