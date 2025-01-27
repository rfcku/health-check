"""Module to manage configuration"""

import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "health_checks_topic")
GROUP_ID = os.getenv("GROUP_ID", "health_checker")

CONSUMER_CONFIG = {
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": GROUP_ID,
    "auto.offset.reset": "earliest",
}

PRODUCER_CONFIG = {
    "bootstrap.servers": KAFKA_BROKER,
    "acks": "all",
}
