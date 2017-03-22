import logging

import requests
from colorama import Fore
from flask import json

from rtxlib import info, error, debug
from rtxlib.changeproviders.ChangeProvider import ChangeProvider


class HTTPRequestChangeProvider(ChangeProvider):
    """ implements a change provider based on HTTP POST requests """

    def __init__(self, wf, cp):
        # load config
        try:
            self.url = cp["url"]
            self.serializer = cp["serializer"]
            info("> HTTPChangePro  | " + self.serializer + " | URL: " + self.url, Fore.CYAN)
        except KeyError:
            error("HTTPChangePro was incomplete")
            exit(1)
        # look at the serializer
        if self.serializer == "JSON":
            self.serialize_function = lambda v: json.dumps(v).encode('utf-8')
        else:
            error("serializer not implemented")
            exit(1)

    def applyChange(self, message):
        """ does a HTTP POST to the URL with the serialized message """
        requests.post(self.url, data=self.serialize_function(message),
                      headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
