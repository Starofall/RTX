from logging import error

from rtxlib.dataproviders.KafkaConsumerDataProvider import KafkaConsumerDataProvider


def init_data_provider(wf):
    cp = wf.system["data_provider"]
    if cp == "kafka_consumer":
        wf.data_provider = KafkaConsumerDataProvider(wf)
    elif cp == "mqtt_listener":
        error("> Not implemented")
    elif cp == "http_data_requests":
        error("> Not implemented")
    else:
        error("Not a valid data_provider")

