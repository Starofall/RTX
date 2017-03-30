import logging

import requests
from colorama import Fore
from flask import json

from rtxlib import info, error, debug
from rtxlib.changeproviders.ChangeProvider import ChangeProvider


class DummyChangeChangeProvider(ChangeProvider):
    """ does not change a system, just prints out the changes"""

    def __init__(self, wf, cp):
        info("> DummyChangePr  | Print Console", Fore.CYAN)
        pass

    def applyChange(self, message):
        info("> DummyChangePr  | " + str(message), Fore.MAGENTA)
