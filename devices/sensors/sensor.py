from abc import ABC, abstractmethod
from mimetypes import init
from multiprocessing.util import abstract_sockets_supported


import pika


class Sensor(ABC):
    def __init__(self, key) -> None:
        self.exchange_name = "EXCHANGE"
        self.key = key

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.exchange_name, exchange_type='direct')

    def __del__(self):
        self.connection.close()

    # @abstractmethod
    # def run(self):
    #     pass
    #     #connection = pika.BlockingConnection(
    #     #    pika.ConnectionParameters(host='localhost'))
    #     #channel = connection.channel()

    #     # self.publish()

    #     # print(" [x] Sent %r" % message)

    @abstractmethod
    def publish(self, key, message):
        # while True:
        #     channel.basic_publish(exchange='', routing_key='', body=message)
        pass
