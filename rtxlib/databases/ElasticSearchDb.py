import traceback

from rtxlib.databases.Database import Database
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elasticsearch.exceptions import TransportError
from elasticsearch.exceptions import ConnectionError
from datetime import datetime
from rtxlib import error


class ElasticSearchDb(Database):

    def __init__(self, db_config):
        self.es = Elasticsearch([{"host": db_config["host"], "port": db_config["port"]}])

        if not self.es.ping():
            error("cannot connect to elasticsearch cluster. Check database configuration in config.json.")
            exit(0)

        index = db_config["index"]
        self.index = index["name"]
        analysis_type = db_config["analysis_type"]
        self.analysis_type_name = analysis_type["name"]
        data_point_type = db_config["data_point_type"]
        self.data_point_type_name = data_point_type["name"]

        mappings = dict()
        if "mapping" in analysis_type:
            # user can specify an type without a mapping (dynamic mapping)
            mappings[self.analysis_type_name] = analysis_type["mapping"]
        if "mapping" in data_point_type:
            # user can specify an type without a mapping (dynamic mapping)
            mappings[self.data_point_type_name] = data_point_type["mapping"]

        body = dict()
        if "settings" in index:
            body["settings"] = index["settings"]
        if mappings:
            body["mappings"] = mappings

        try:
            self.indices_client = IndicesClient(self.es)
            if not self.indices_client.exists(self.index):
                self.indices_client.create(self.index, body)
        except TransportError:
            error("Error while creating elasticsearch. Check type mappings in config.json.")
            print(traceback.format_exc())
            exit(0)

    def save_analysis(self, name, strategy):
        body = dict()
        body["name"] = name
        body["strategy"] = strategy
        body["created"] = datetime.now()
        try:
            res = self.es.index(self.index, self.analysis_type_name, body)
            return res['_id']
        except ConnectionError:
            error("Error while saving analysis data in elasticsearch. Check connection to elasticsearch and restart.")
            exit(0)

    def save_data_point(self, exp_run, knobs, payload, data_point_count, analysis_id):
        data_point_id = analysis_id + "#" + str(exp_run) + "_" + str(data_point_count)
        body = dict()
        body["exp_run"] = exp_run
        body["knobs"] = knobs
        body["payload"] = payload
        body["created"] = datetime.now()
        try:
            self.es.index(self.index, self.data_point_type_name, body, data_point_id, parent=analysis_id)
        except ConnectionError:
            error("Error while saving data point data in elasticsearch. Check connection to elasticsearch.")

    def get_data_points(self, analysis_id, exp_run):
        query = {
            "query": {
                "parent_id" : {
                    "type": "data_point",
                    "id" : str(analysis_id)
                }
            },
            "post_filter": {
                "term": { "exp_run": int(exp_run) }
            }
        }
        self.indices_client.refresh()
        res = self.es.search(self.index, self.data_point_type_name, query)
        return [data["_source"]["payload"] for data in res["hits"]["hits"]]

    def save_analysis_result(self, analysis_id, result):
        result_dict = {"result": result}
        body = {"doc": result_dict}
        try:
            self.es.update(self.index, self.analysis_type_name, analysis_id, body)
        except ConnectionError:
            error("Error while updating analysis data in elasticsearch. Check connection to elasticsearch.")
