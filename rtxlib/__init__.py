from __future__ import print_function

import os

from colorama import Fore

import sys

LEVEL_DEBUG = 4
LEVEL_INFO = 3
LEVEL_WARN = 2
LEVEL_ERROR = 1
LEVEL_NONE = 0

LOG_LEVEL = 3

def debug(any, color=Fore.CYAN):
    if LOG_LEVEL >= LEVEL_DEBUG:
        print(color + str(any) + Fore.RESET)


def info(any, color=Fore.GREEN):
    if LOG_LEVEL >= LEVEL_INFO:
        print(color + str(any) + Fore.RESET)


def warn(any, color=Fore.YELLOW):
    if LOG_LEVEL >= LEVEL_WARN:
        print(color + str(any) + Fore.RESET)


def error(any, color=Fore.RED):
    if LOG_LEVEL >= LEVEL_ERROR:
        print(color + "Error: " + str(any) + Fore.RESET)


def process(preText, i, total):
    sys.stdout.write('\r')
    sys.stdout.flush()
    size_str = Fore.YELLOW + "> " + preText + "["
    percentage = 30 * i / total
    for j in range(0, percentage):
        size_str += "#"
    for k in range(percentage, 30):
        size_str += "."
    size_str += "] Target: " + str(total) + " | Done: " + str(i) + Fore.RESET
    sys.stdout.write('%s\r' % size_str)
    sys.stdout.flush()



def inline_print(str):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write('%s\r' % str)
    sys.stdout.flush()

def direct_print(str):
    import sys
    sys.stdout.write(str)
    sys.stdout.flush()


import csv
def log_results(experiment_folder, data, append=True):
    try:
        if append:
            with open('./' + str(experiment_folder) + '/results.csv', 'ab') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                writer.writerow(data)
        else:
            with open('./' + str(experiment_folder) + '/results.csv', 'wb') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                writer.writerow(data)

    except csv.Error as e:
        error("Log to csv did not work: " + str(e))
        pass
