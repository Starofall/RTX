#!/usr/bin/python
import sys
import imp

import rtxlib

from rtxlib import info, error, debug
from rtxlib.workflow import execute_workflow
from rtxlib.report import plot

if __name__ == '__main__':
    # Throw error on to less parameters
    if len(sys.argv) == 1:
        error("missing parameter /  | try >python rtx.py help")
        exit(1)

    # Parse the requested command
    cmd = sys.argv[1]

    if cmd == "start" or cmd == "report":
        if len(sys.argv) != 3:
            error("missing experiment folder")
            exit(1)
        # predefine a default workflow
        wf = None
        try:
            wf = imp.load_source('wf', './' + sys.argv[2] + '/definition.py')
            wf.folder = sys.argv[2]
            testName = wf.name
        except IOError:
            error("Folder is not valid")
            exit(1)
        except AttributeError:
            error("Workflow did not had a name attribute")
            exit(1)
        except ImportError as e:
            error("Import failed: " + str(e))
            exit(1)
        # setting global variable log_folder for logging and clear log
        rtxlib.LOG_FOLDER = wf.folder
        rtxlib.clearOldLog()
        # look at the command
        if cmd == "start":
            info("> Starting RTX experiment...")
            # Call WorkflowExecutor on the loaded workflow
            execute_workflow(wf)
            plot(wf)
            exit(0)
        if cmd == "report":
            info("> Starting RTX reporting...")
            plot(wf)
            exit(0)

    # Help
    info("#################")
    info("# RTX Help Page #")
    info("#################")
    info(" >python rtx.py help          -> shows this page ")
    info("         rtx.py start $folder -> runs the experiment in this folder")
    info("#################")
    exit(0)
