import logging
from colorama import Fore

from rtxlib import info, error, debug
from rtxlib.changeproviders.ChangeProvider import ChangeProvider

class KafkaProducerChangeProvider(ChangeProvider):
    def __init__(self, wf):
        from kafka import KafkaProducer
        from flask import json
        try:
            self.kafka_uri = wf.configuration["kafka_producer"]["kafka_uri"]
            self.topic = wf.configuration["kafka_producer"]["topic"]
            self.serializer = wf.configuration["kafka_producer"]["serializer"]
            info(
                "> KafkaProducer  | " + self.serializer + " | URI: " + self.kafka_uri + " | Topic: " +
                self.topic, Fore.CYAN)
        except KeyError:
            error("configuration.kafka_producer was incomplete")
            exit(1)
        # look at the serializer
        if self.serializer == "JSON":
            self.serialize_function = lambda v: json.dumps(v).encode('utf-8')
        else:
            error("serializer not implemented")
            exit(1)
        # try to connect
        try:
            logging.getLogger("kafka.coordinator.consumer").setLevel("ERROR")
            logging.getLogger("kafka.conn").setLevel("ERROR")
            self.producer = KafkaProducer(bootstrap_servers=self.kafka_uri,
                                          value_serializer=self.serialize_function,
                                          request_timeout_ms=5000)
        except:
            error("connection to kafka failed")
            exit(1)

    def applyChange(self, message):
        debug("Sending out Kafka Message:" + str(message))
        self.producer.send(self.topic, message)
