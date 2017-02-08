from logging import error

from rtxlib.dataproviders.KafkaConsumerDataProvider import KafkaConsumerDataProvider


def init_data_providers(wf):
    cp = wf.primary_data_provider
    if cp["type"] == "kafka_consumer":
        cp["instance"] = KafkaConsumerDataProvider(wf,cp)
    elif cp["type"] == "mqtt_listener":
        error("> Not implemented")
    elif cp["type"] == "http_data_requests":
        error("> Not implemented")
    else:
        error("Not a valid data_provider")

