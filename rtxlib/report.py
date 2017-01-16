from colorama import Fore
from rtxlib import info, error

import pandas as pd
import seaborn as sns
import csv


def plot(wf):

    info("######################################", Fore.CYAN)
    info("> Reporting on   | " + str(wf.name), Fore.CYAN)

    plot_file_dir = './' + str(wf.folder)

    try:
        with open('./' + str(plot_file_dir) + '/results.csv', 'r') as csv_file:
            reader = csv.reader(csv_file, dialect='excel')
            header = next(reader)
    except IOError:
        error( 'Please first generate a "' + str(plot_file_dir) + '/results.csv" file by running the start command')
        return

    results_dataframe = pd.read_csv('./' + str(wf.folder) + '/results.csv')

    if len(header) == 2:

        info("> Found 1 knob, creating scatter plot...", Fore.CYAN)

        plot_file = plot_file_dir + '/scatter_plot.png'
        ax = sns.regplot(x=header[0], y=header[1], data=results_dataframe, fit_reg=False)
        fig = ax.get_figure()
        fig.savefig(plot_file)

        info("> Plot saved at " + plot_file, Fore.CYAN)

    elif len(header) == 3:

        info("> Found 2 knobs, creating heatmap...", Fore.CYAN)

        plot_file = plot_file_dir + '/heatmap.png'

        results = results_dataframe.pivot(*header)

        ax = sns.heatmap(results, annot=True, fmt=".4f", linewidths=.5)
        fig = ax.get_figure()
        fig.savefig(plot_file)
        fig.show()

        info("> Plot saved at " + plot_file, Fore.CYAN)

    else:
        info("> Cannot plot these results (RTX can only plot experiments of one of two variables for now)", Fore.CYAN)
