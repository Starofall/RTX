#!/usr/bin/python
import analysis_lib

from analysis_lib.TtestAnalysis import TtestAnalysis
from analysis_lib import setup_database

if __name__ == '__main__':

    setup_database()
    ttestAnalysis = TtestAnalysis(alpha=0.05)
    ttestAnalysis.run()