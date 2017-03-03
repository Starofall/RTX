from logging import error

from rtxlib.dataproviders.KafkaConsumerDataProvider import KafkaConsumerDataProvider
from rtxlib.dataproviders.MQTTListenerDataProvider import MQTTListenerDataProvider


def init_data_providers(wf):
    createInstance(wf, wf.primary_data_provider)
    for cp in wf.secondary_data_providers:
        createInstance(wf, cp)


def createInstance(wf, cp):
    if cp["type"] == "kafka_consumer":
        cp["instance"] = KafkaConsumerDataProvider(wf, cp)
    elif cp["type"] == "mqtt_listener":
        cp["instance"] = MQTTListenerDataProvider(wf, cp)
    elif cp["type"] == "http_data_requests":
        error("> Not implemented")
    else:
        error("Not a valid data_provider")
