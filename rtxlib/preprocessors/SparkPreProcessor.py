import atexit
import os
import subprocess
import time

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
        # starting a subprocess to allow termination of spark after we are done
        self.process = subprocess.Popen(spark_home + spark_bin + ' --class ' + self.job_class + \
                                        ' ./' + wf.folder + '/' + self.job_file, stdout=subprocess.PIPE, shell=True)
        atexit.register(self.shutdown)
        time.sleep(10)

    def shutdown(self):
        try:
            # @todo removing the spark processor on windows after running just works this way atm
            subprocess.Popen("taskkill /f /im java.exe", shell=True)
        except:
            pass
        try:
            self.process.kill()
        except:
            pass
