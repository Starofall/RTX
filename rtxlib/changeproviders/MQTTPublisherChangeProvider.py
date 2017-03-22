import logging
from colorama import Fore
from paho import mqtt
from paho.mqtt import publish

from rtxlib import info, error, debug
from rtxlib.changeproviders.ChangeProvider import ChangeProvider
from flask import json

class MQTTPublisherChangeProvider(ChangeProvider):
    """ implements a change providers using MQTT """
    def __init__(self, wf, cp):
        # load config
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
        """ publish a single mqtt message to the server """
        publish.single(self.topic, payload=self.serialize_function(message), qos=0,
                       retain=False, hostname=self.host, port=self.port)
