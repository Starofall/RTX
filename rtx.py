#!/usr/bin/python
import sys
import imp
import json
import rtxlib

from colorama import Fore
from rtxlib import info, error, debug
from rtxlib.workflow import execute_workflow
from rtxlib.report import plot
from rtxlib.databases import create_instance
from rtxlib.databases import get_no_database


def loadDefinition(folder):
    """ opens the given folder and searches for a definition.py file and checks if it looks valid"""
    if len(sys.argv) != 3:
        error("missing experiment folder")
        exit(1)
    try:
        wf = imp.load_source('wf', './' + folder + '/definition.py')
        wf.folder = sys.argv[2]
        testName = wf.name
        return wf
    except IOError:
        error("Folder is not a valid experiment folder (does not contain definition.py)")
        exit(1)
    except AttributeError:
        error("Workflow did not had a name attribute")
        exit(1)
    except ImportError as e:
        error("Import failed: " + str(e))
        exit(1)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == "start":
        wf = loadDefinition(sys.argv[2])

        with open('rtx_config.json') as json_data_file:
            try:
                config_data = json.load(json_data_file)
            except ValueError:
                # config.json is empty - default configuration used
                config_data = []

        # check for database configuration
        if "database" in config_data:
            database_config = config_data["database"]
            info("> RTX configuration: Using " + database_config["type"] + " database.", Fore.CYAN)
            db = create_instance(database_config)
            wf.rtx_run_id = db.save_rtx_run(wf.execution_strategy)
            wf.db = db
        else:
            info("> RTX configuration: No database specified.", Fore.CYAN)
            wf.rtx_run_id = "-1"
            wf.db = get_no_database()

        # setting global variable log_folder for logging and clear log
        rtxlib.LOG_FOLDER = wf.folder
        rtxlib.clearOldLog()
        info("> Starting RTX experiment...")

        execute_workflow(wf)
        plot(wf)
        exit(0)
    if len(sys.argv) > 2 and sys.argv[1] == "report":
        wf = loadDefinition(sys.argv[2])
        info("> Starting RTX reporting...")
        plot(wf)
        exit(0)

    # Help
    info("RTX Help Page")
    info("COMMANDS:")
    info("> python rtx.py help           -> shows this page ")
    info("         rtx.py start  $folder -> runs the experiment in this folder")
    info("         rtx.py report $folder -> shows the reports for the experiment in this folder")
    info("EXAMPLE:")
    info("> python rtx.py start ./examples/http-gauss")
    exit(0)
else:
    print("Please start this file with > python rtx.py ...")
