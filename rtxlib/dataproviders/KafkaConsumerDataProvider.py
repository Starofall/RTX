import logging
from colorama import Fore
from kafka import KafkaConsumer
from flask import json
from rtxlib import info, error, debug, warn, direct_print, inline_print
from rtxlib.dataproviders.DataProvider import DataProvider


class KafkaConsumerDataProvider(DataProvider):
    """ implements a data provider for kafaka """

    def __init__(self, wf, cp):
        self.callBackFunction = None
        # load config
        try:
            self.kafka_uri = cp["kafka_uri"]
            self.topic = cp["topic"]
            self.serializer = cp["serializer"]
            info(
                "> KafkaConsumer  | " + self.serializer + " | URI: " + self.kafka_uri + " | Topic: " +
                self.topic, Fore.CYAN)
        except KeyError as e:
            error("system.kafkaConsumer was incomplete: " + str(e))
            exit(1)
        # look at the serializer
        if self.serializer == "JSON":
            self.serialize_function = lambda m: json.loads(m.decode('utf-8'))
        else:
            error("serializer not implemented")
            exit(1)
        # try to connect
        try:
            # disable annoying logging
            logging.getLogger("kafka.coordinator.consumer").setLevel("ERROR")
            logging.getLogger("kafka.conn").setLevel("ERROR")
            # connect to kafka
            self.consumer = KafkaConsumer(bootstrap_servers=self.kafka_uri,
                                          value_deserializer=self.serialize_function,
                                          enable_auto_commit=False,
                                          group_id=None,
                                          consumer_timeout_ms=3000)
            # subscribe to the requested topic
            self.consumer.subscribe([self.topic])
        except RuntimeError as e:
            error("connection to kafka failed: " + str(e))
            exit(1)

    def reset(self):
        """ creates a new consumer to get to the current position of the queue """
        try:
            self.consumer.close()
            self.consumer = KafkaConsumer(bootstrap_servers=self.kafka_uri,
                                          value_deserializer=self.serialize_function,
                                          group_id=None,
                                          consumer_timeout_ms=3000)
            self.consumer.subscribe([self.topic])
        except RuntimeError as e:
            error("connection to kafka failed: " + str(e))
            exit(1)

    def returnData(self):
        """ returns the next data (blocking) """
        try:
            return next(self.consumer).value
        except StopIteration:
            inline_print(
                Fore.RED + "> WARNING - No message present within three seconds                          " + Fore.RESET)
            return None

    def returnDataListNonBlocking(self):
        """ polls for 5ms and returns all messages that came in """
        try:
            values = []
            partitions = self.consumer.poll(5)
            if len(partitions) > 0:
                for p in partitions:
                    for response in partitions[p]:
                        values.append(response.value)
            return values
        except StopIteration:
            return None
