# Abstract interface for a data provider
#
# A data provider gets data out of the system into RTX to be analyzed


class DataProvider:
    def __init__(self, wf):
        pass

    def reset(self):
        """ called before a experiment starts to e.g. clear a queue """
        pass

    def returnData(self):
        """ returns a single value from the queue OR from a rest call """
        pass

    def returnDataListNonBlocking(self):
        """ returns a list of all available data without waiting for it """
        pass
