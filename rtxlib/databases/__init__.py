from rtxlib.databases import Database
from rtxlib.databases.ElasticSearchDb import ElasticSearchDb
from rtxlib.databases.NoDatabase import NoDatabase


def create_instance(database_config):
    """ creates a single instance of a database  """
    if database_config["type"] == "elasticsearch":
        return ElasticSearchDb(database_config)


def get_no_database():
    return NoDatabase()
