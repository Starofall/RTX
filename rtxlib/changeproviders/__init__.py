from rtxlib import error
from rtxlib.changeproviders.KafkaProducerChangeProvider import KafkaProducerChangeProvider
from rtxlib.changeproviders.MQTTPublisherChangeProvider import MQTTPublisherChangeProvider


def init_change_provider(wf):
    """ loads the specified change provider into the workflow """
    cp = wf.change_provider
    if cp["type"] == "kafka_producer":
        cp["instance"] = KafkaProducerChangeProvider(wf, cp)
    elif cp["type"] == "mqtt_publisher":
        cp["instance"] = MQTTPublisherChangeProvider(wf, cp)
    elif cp["type"] == "http_change_requests":
        error("> Not implemented")
        exit(1)
    else:
        error("Not a valid changeProvider")
        exit(1)
