from rtxlib import info, error, debug, warn, direct_print, inline_print
from rtxlib.dataproviders.DataProvider import DataProvider


class LocalHookChangeProvider(DataProvider):

    def __init__(self, wf, cp):
        self.getResultsHook = cp["getResultsHook"]

    def returnData(self):
        return self.getResultsHook()

    def returnDataListNonBlocking(self):
        pass
