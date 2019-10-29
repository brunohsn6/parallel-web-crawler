from kafka import KafkaProducer
import json
import pprint
import logging
import time

class KafkaProducer:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers,value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    def execute(self, message):
        self.producer.send("CRAWLER_DOWNLOAD", message)

#self.producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092',value_serializer=lambda x: json.dumps(x).encode('utf-8'))
