from rtxlib import error
from rtxlib.changeproviders.KafkaProducerChangeProvider import KafkaProducerChangeProvider


def init_change_provider(wf):
    """ loads the specified change provider into the workflow """
    cp = wf.system["change_provider"]
    if cp == "kafka_producer":
        wf.change_provider = KafkaProducerChangeProvider(wf)
    elif cp == "mqtt_publisher":
        error("> Not implemented")
        exit(1)
    elif cp == "http_change_requests":
        error("> Not implemented")
        exit(1)
    else:
        error("Not a valid changeProvider")
        exit(1)
