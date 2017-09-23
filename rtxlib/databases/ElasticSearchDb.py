from rtxlib.databases.Database import Database
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
from rtxlib import error


class ElasticSearchDb(Database):

    def __init__(self, host, port):
        self.es = Elasticsearch([{"host": host, "port": port}])
        if not self.es.ping():
            error("cannot connect to elasticsearch cluster. Check database configuration in config.json.")
            exit(0)

    def save_with_id(self, data):
        try:
            self.es.index(index=data["index"], doc_type=data["doc_type"], id=data["id"], body=data["body"])
        except ConnectionError:
            error("error while updating elasticsearch index")

    def save_without_id(self, data):
        try:
            res = self.es.index(index=data["index"], doc_type=data["doc_type"], body=data["body"])
            return res['_id']
        except ConnectionError:
            error("error while updating elasticsearch index")
