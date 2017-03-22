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
    """ implements a data provider based on http """

    def __init__(self, wf, cp):
        self.callBackFunction = None
        # load config
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
        """ does a http GET request and returns the result value """
        try:
            r = requests.get(self.url)
            return self.serialize_function(r.content)
        except:
            error("HTTP Connection Problems")
            return None

    def returnDataListNonBlocking(self):
        """ by logic this can not be non-blocking, so it is implemented as returnData """
        try:
            r = requests.get(self.url)
            return [self.serialize_function(r.content)]
        except:
            error("HTTP Connection Problems")
            return None
