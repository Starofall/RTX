from time import sleep

import logging

import requests
from colorama import Fore
from flask import json
from paho import mqtt
import paho.mqtt.client as mqtt

from rtxlib import info, error, debug, warn, direct_print, inline_print
from rtxlib.dataproviders.DataProvider import DataProvider


class HTTPRequestDataProvider(DataProvider):
    def __init__(self, wf, cp):
        self.callBackFunction = None
        try:
            self.url = cp["url"]
            self.serializer = cp["serializer"]
            info("> HTTPDataPro    | " + self.serializer + " | URL: " + self.url, Fore.CYAN)
        except KeyError as e:
            error("HTTPDataPro definition was incomplete: " + str(e))
            exit(1)
        if self.serializer == "JSON":
            self.serialize_function = lambda m: json.loads(m.decode('utf-8'))
        else:
            error("serializer not implemented")
            exit(1)

    def returnData(self):
        try:
            r = requests.get(self.url)
            return self.serialize_function(r.content)
        except:
            error("HTTP Connection Problems")
            return None

    def returnDataListNonBlocking(self):
        # returns the full queue and empties it
        values = self.queue
        self.queue = []
        return values
