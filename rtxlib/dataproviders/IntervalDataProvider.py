from time import sleep

import logging

import requests
from colorama import Fore
from flask import json
from paho import mqtt
import paho.mqtt.client as mqtt

from rtxlib import info, error, debug, warn, direct_print, inline_print
from rtxlib.dataproviders.DataProvider import DataProvider
from time import sleep


class IntervalDataProvider(DataProvider):
    """ implements a dummy data provider that returns data every second """

    def __init__(self, wf, cp):
        self.timer = 0
        # load config
        try:
            self.seconds = cp["seconds"]
            info("> Interval       | Seconds: " + str(self.seconds), Fore.CYAN)
        except KeyError as e:
            error("IntervalDataProvider definition was incomplete: " + str(e))
            exit(1)

    def returnData(self):
        """ does wait for x seconds and then return the timer counter value """
        self.timer += 1
        sleep(self.seconds)
        return self.timer

    def returnDataListNonBlocking(self):
        """ does wait for x seconds and then return the timer counter value """
        error("IntervalDataProvider is not able to work as a secondary data provider")
        exit(1)