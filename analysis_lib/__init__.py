import json
import analysis_lib

from colorama import Fore
from rtxlib import info, error, debug
from rtxlib.databases import create_instance

DB = None


def setup_database():

    with open('oeda_config.json') as json_data_file:
        try:
            config_data = json.load(json_data_file)
        except ValueError:
            error("> You need to specify a database configuration in oeda_config.json.")
            exit(0)

    if "database" not in config_data:
        error("You need to specify a database configuration in oeda_config.json.")
        exit(0)

    database_config = config_data["database"]
    info("> OEDA configuration: Using " + database_config["type"] + " database.", Fore.CYAN)
    analysis_lib.DB = create_instance(database_config)


def db():
    if not DB:
        error("You have to setup the database.")
        exit(0)
    return DB