from rtxlib.databases import Database
from rtxlib.databases.ElasticSearchDb import ElasticSearchDb

def createInstance(config):
    """ creates a single instance of a data provider and stores the instance as reference in the definition """
    if config["type"] == "elasticsearch":
        return ElasticSearchDb(config["host"], config["port"])
