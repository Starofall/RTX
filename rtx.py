#!/usr/bin/python
import sys
import imp
from elasticsearch import Elasticsearch
from datetime import datetime

import rtxlib

from rtxlib import info, error, debug
from rtxlib.workflow import execute_workflow
from rtxlib.report import plot


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

        es = Elasticsearch()
        res = es.index(index="rtx-analysis", doc_type=wf.type, body=wf.execution_strategy)

        # setting global variable log_folder for logging and clear log
        rtxlib.LOG_FOLDER = wf.folder
        rtxlib.clearOldLog()
        info("> Starting RTX experiment...")

        wf.es = es
        wf.dt = datetime
        wf.analysis_id = res['_id']

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
