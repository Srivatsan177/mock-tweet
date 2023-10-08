import os

from kafka import KafkaProducer


def get_kafka_producer():
    kafka_producer = KafkaProducer(bootstrap_servers=[os.environ["KAFKA_HOST"]])
    return kafka_producer
