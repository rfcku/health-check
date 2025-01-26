
from confluent_kafka import Producer, Consumer 
from confluent_kafka.cimpl import KafkaError

from config import PRODUCER_CONFIG, CONSUMER_CONFIG, KAFKA_TOPIC
from datetime import datetime
import json
import logging
import time

logging.basicConfig(level=logging.DEBUG)

def get_data():
    data = {
        "serviceName": "MyService",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "OK",
    }
    logging.debug(f"Data: {data}")
    return data

class Kafka:
    def __init__(self):
        self.producer = Producer(PRODUCER_CONFIG)
        self.consumer = Consumer(CONSUMER_CONFIG)
        self.topic = KAFKA_TOPIC
        self.messages = []

    def get_messages(self):
        m = []
        for message in self.messages:
            try:
                m.append(json.loads(message))
            except Exception as e:
                logging.error(f"Error parsing message: {e}")
        return m

    def get_last_message(self):
        if len(self.messages) > 0:
            try:
                return json.loads(self.messages[-1])
            except Exception as e:
                logging.error(f"Error parsing message: {e}")
        return None

    def delivery_callback(self, err, msg):
        if err:
            logging.error(f"ERROR: Message failed delivery: {err}")
        else:
            logging.info("Produced event to topic")
        return True

    def produce(self):
        logging.info("Starting Kafka producer")
        try:
            while True:
                data = get_data()
                logging.info(f"Producing message to Kafka {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self.producer.produce(self.topic, json.dumps(data), callback=self.delivery_callback)
                self.producer.poll(0)
                self.producer.flush()
                time.sleep(1)
        except Exception as e:
            logging.error(f"Kafka producer exception: {e}")


    def consume(self):
        logging.info("Starting Kafka consumer")
        try:
            self.consumer.subscribe([self.topic])
            logging.info(f"Subscribed to topic. {self.topic}")
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logging.error(f"Kafka error: {msg.error()}")
                        continue
                try:
                    message = msg.value().decode("utf-8")
                    self.messages.append(message)
                    logging.info(f"Consumed message: {message}")
                except Exception as e:
                    logging.error(f"Error processing message: {e}")

        except Exception as e:
            logging.error(f"Kafka consumer exception: {e}")
        finally:
            self.consumer.close()
        
if __name__ == "__main__":
    kafka = Kafka()
    kafka.produce()
