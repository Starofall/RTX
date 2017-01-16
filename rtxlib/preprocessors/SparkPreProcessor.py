import atexit
import os
import platform
import subprocess
import time

import sys
from colorama import Fore

from rtxlib import info, error
from rtxlib.preprocessors.PreProcessor import PreProcessor


class SparkPreProcessor(PreProcessor):
    """ Implements a preprocessor in spark """

    def __init__(self, wf):
        try:
            self.submit_mode = wf.configuration["spark"]["submit_mode"]
            self.job_file = wf.configuration["spark"]["job_file"]
            self.job_class = wf.configuration["spark"]["job_class"]
            info("> PreProcessor   | Spark  | Mode: " + str(self.submit_mode) + " | Args: " + str(
                self.job_class), Fore.CYAN)
        except KeyError as e:
            error("configuration.spark was incomplete: " + str(e))
            exit(1)
        spark_home = os.environ.get("SPARK_HOME")
        spark_bin = "/bin/spark-submit"

        # http://stackoverflow.com/questions/13243807/popen-waiting-for-child-process-even-when-the-immediate-child-has-terminated/13256908#13256908
        # set system/version dependent "start_new_session" analogs
        kwargs = {}
        if platform.system() == 'Windows':
            # from msdn [1]
            CREATE_NEW_PROCESS_GROUP = 0x00000200  # note: could get it from subprocess
            DETACHED_PROCESS = 0x00000008  # 0x8 | 0x200 == 0x208
            kwargs.update(creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
        elif sys.version_info < (3, 2):  # assume posix
            kwargs.update(preexec_fn=os.setsid)
        else:  # Python 3.2+ and Unix
            kwargs.update(start_new_session=True)
        # starting a subprocess to allow termination of spark after we are done
        self.process = subprocess.Popen(spark_home + spark_bin + ' --class ' + self.job_class + \
                                        ' ./' + wf.folder + '/' + self.job_file, stdout=subprocess.PIPE, shell=True,**kwargs)
        atexit.register(self.shutdown)
        time.sleep(10)

    def shutdown(self):
        try:
            self.process.kill()
        except:
            pass
