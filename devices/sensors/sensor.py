from abc import ABC, abstractmethod
import string
import threading
import time


import pika
from utils import kExchange, kIP


class Sensor(ABC):
    def __init__(self, key) -> None:
        self.key = key
        self.info = None

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=kIP))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=kExchange, exchange_type='direct')

        self.publisher = threading.Thread(
            target=self.publish, args=[key])
        self.publisher.start()

    def __del__(self):
        self.connection.close()

    def publish(self, key):
        while True:
            self.calculate()
            self.channel.basic_publish(
                exchange=kExchange, routing_key=key, body=self.get_info())
            print(f"Message sent: {self.get_info()}")
            time.sleep(5)

    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def get_info(self):
        pass
