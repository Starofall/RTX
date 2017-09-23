# Abstract interface for a database
#
# A database stores the raw data and the experiment runs of RTX.


class Database:

    def __init__(self):
        pass

    def save_with_id(self, data, id):
        """ called for saving experiment configuration runs and raw data """
        pass

    def save_without_id(self, data):
        """ saves the data and returns the auto-generated id """
        pass

