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
        rtx_run_type = db_config["rtx_run_type"]
        self.rtx_run_type_name = rtx_run_type["name"]
        analysis_type = db_config["analysis_type"]
        self.analysis_type_name = analysis_type["name"]
        data_point_type = db_config["data_point_type"]
        self.data_point_type_name = data_point_type["name"]

        mappings = dict()
        # user can specify an type without a mapping (dynamic mapping)
        if "mapping" in rtx_run_type:
            mappings[self.rtx_run_type_name] = rtx_run_type["mapping"]
        if "mapping" in analysis_type:
            mappings[self.analysis_type_name] = analysis_type["mapping"]
        if "mapping" in data_point_type:
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

    def save_rtx_run(self, strategy):
        body = dict()
        body["strategy"] = strategy
        body["created"] = datetime.now()
        try:
            res = self.es.index(self.index, self.rtx_run_type_name, body)
            return res['_id']
        except ConnectionError:
            error("Error while saving rtx_run data in elasticsearch. Check connection to elasticsearch and restart.")
            exit(0)

    def update_rtx_run(self, rtx_run_id, exp_count, list_of_configurations=None):
        doc = dict()
        doc["exp_count"] = exp_count

        if list_of_configurations:
            doc["list_of_configurations"] = list_of_configurations

        body = {"doc": doc}
        try:
            self.es.update(self.index, self.rtx_run_type_name, rtx_run_id, body)
        except ConnectionError:
            error("Error while updating rtx_run data in elasticsearch. Check connection to elasticsearch.")

    def get_exp_count(self, rtx_run_id):
        return self.get_run_configuration_info(rtx_run_id, "exp_count")

    def get_list_of_configurations(self, rtx_run_id):
        return self.get_run_configuration_info(rtx_run_id, "list_of_configurations")

    def get_sample_size(self, rtx_run_id):
        strategy = self.get_run_configuration_info(rtx_run_id, "strategy")
        return strategy["sample_size"]

    def get_run_configuration_info(self, rtx_run_id, field):
        res = self.es.get(self.index, rtx_run_id, self.rtx_run_type_name, _source=[field])
        if field in res["_source"]:
            return res["_source"][field]
        else:
            error("'" + field + "' does not exist in rtx run with id " + rtx_run_id)
            return 0


    def save_data_point(self, exp_run, knobs, payload, data_point_count, rtx_run_id):
        data_point_id = rtx_run_id + "#" + str(exp_run) + "_" + str(data_point_count)
        body = dict()
        body["exp_run"] = exp_run
        body["knobs"] = knobs
        body["payload"] = payload
        body["created"] = datetime.now()
        try:
            self.es.index(self.index, self.data_point_type_name, body, data_point_id, parent=rtx_run_id)
        except ConnectionError:
            error("Error while saving data point data in elasticsearch. Check connection to elasticsearch.")

    def get_data_points(self, rtx_run_id, exp_run):
        query = {
            "query": {
                "parent_id" : {
                    "type": "data_point",
                    "id" : str(rtx_run_id)
                }
            },
            "post_filter": {
                "term": { "exp_run": int(exp_run) }
            }
        }
        self.indices_client.refresh()
        res = self.es.search(self.index, self.data_point_type_name, query)
        return [data["_source"]["payload"] for data in res["hits"]["hits"]]

    def save_analysis(self, rtx_run_ids, name, result):
        ids_str = reduce(lambda a,b: a+"+"+b, rtx_run_ids[1:], rtx_run_ids[0])
        analysis_id = ids_str + "_" + name
        body = dict()
        body["rtx_run_ids"] = rtx_run_ids
        body["name"] = name
        body["result"] = result
        body["created"] = datetime.now()
        try:
            self.es.index(self.index, self.analysis_type_name, body, analysis_id)
        except ConnectionError:
            error("Error while saving analysis data in elasticsearch. Check connection to elasticsearch.")
