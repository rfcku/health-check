# pylint: disable=import-error, no-member, broad-except, protected-access, no-else-continue
"""Module to produce and consume messages to Kafka topic"""


import json
import logging
import time
from datetime import datetime

import kubernetes
from confluent_kafka import Producer, Consumer
from confluent_kafka.cimpl import KafkaError
from config import PRODUCER_CONFIG, CONSUMER_CONFIG, KAFKA_TOPIC

logging.basicConfig(level=logging.DEBUG)

def get_data():
    """Function to generate data to be sent to Kafka"""
    # try:
    #     kubernetes.config.load_kube_config()
    # except:
    #     kubernetes.config.load_incluster_config()
    #
    # v1 = kubernetes.client.CoreV1Api()
    #
    # pods = v1.list_pod_for_all_namespaces(watch=False)
    # data = []
    # for pod in pods.items:
    #     data.append({
    #         "serviceName": pod.metadata.name,
    #         "status": pod.status.phase,
    #         "timestamp": pod.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    #     })
    data = []
    for i in range(10):
        data.append({
            "serviceName": "service" + str(i),
            "status": "Running",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    return data


class Kafka:
    """Class to produce and consume messages to Kafka topic"""

    def __init__(self):
        self.producer = Producer(PRODUCER_CONFIG)
        self.consumer = Consumer(CONSUMER_CONFIG)
        self.topic = KAFKA_TOPIC
        self.messages = []

    def get_messages(self):
        """Method to return all messages consumed from Kafka"""
        m = []
        for message in self.messages:
            try:
                m.append(json.loads(message))
            except Exception as e:
                logging.error("Error parsing message: %s", e)
        return m

    def get_last_message(self):
        """Method to return the last message consumed from Kafka"""
        if len(self.messages) > 0:
            try:
                return json.loads(self.messages[-1])
            except Exception as e:
                logging.error("Error parsing message: %s", e)
        return []

    def delivery_callback(self, err, msg):
        """Method to handle delivery callback"""
        if err:
            logging.error("ERROR: Message failed delivery: %s", err)
        else:
            logging.info("Produced event to topici %s", msg.topic())
        return True

    def produce(self):
        """Method to produce messages to Kafka"""
        logging.info("Starting Kafka producer")
        try:
            while True:
                pods = get_data()
                logging.info("Producing message to Kafka")
                for data in pods:
                    self.producer.produce(
                        self.topic, json.dumps(data), callback=self.delivery_callback
                    )
                self.producer.poll(0)
                self.producer.flush()
                time.sleep(1)
        except Exception as e:
            logging.error("Kafka producer exception: %s", e)

    def consume(self):
        """Method to consume messages from Kafka"""
        logging.info("Starting Kafka consumer")
        try:
            self.consumer.subscribe([self.topic])
            logging.info("Subscribed to topic: %s", self.topic)
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logging.error("Kafka error: %s", msg.error())
                        continue
                try:
                    message = msg.value().decode("utf-8")
                    logging.info("Consumed message: %s", message)
                    self.messages.append(message)
                except Exception as e:
                    logging.error("Error processing message: %s", e)

        except Exception as e:
            logging.error("Kafka consumer exception: %s", e)
        finally:
            self.consumer.close()


if __name__ == "__main__":
    kafka = Kafka()
    kafka.produce()
