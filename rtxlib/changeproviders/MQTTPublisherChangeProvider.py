import logging
from colorama import Fore
from paho import mqtt
from paho.mqtt import publish

from rtxlib import info, error, debug
from rtxlib.changeproviders.ChangeProvider import ChangeProvider


class MQTTPublisherChangeProvider(ChangeProvider):
    def __init__(self, wf, cp):
        from flask import json
        try:
            self.queue = []
            self.host = cp["host"]
            self.port = cp["port"]
            self.topic = cp["topic"]
            self.serializer = cp["serializer"]
            info("> MQTTPublisher  | " + self.serializer + " | URI: " + self.host + ":" + self.port + " | Topic: " +
                 self.topic, Fore.CYAN)
        except KeyError:
            error("mqttPublisher definition was incomplete")
            exit(1)
        # look at the serializer
        if self.serializer == "JSON":
            self.serialize_function = lambda v: json.dumps(v).encode('utf-8')
        else:
            error("serializer not implemented")
            exit(1)

    def applyChange(self, message):
        publish.single(self.topic, payload=self.serialize_function(message), qos=0,
                       retain=False, hostname=self.host, port=self.port)
