
class DataProvider:
    def __init__(self, wf):
        pass

    def reset(self):
        """ called before a experiment starts to e.g. clear a queue """
        pass

    def returnData(self):
        """ returns a single value from the queue OR from a rest call """
        pass
