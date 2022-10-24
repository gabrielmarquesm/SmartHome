from concurrent import futures
from enum import Enum
import threading

import grpc
import pika

import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc
from devices.actuators.AC import ACService

kPort = "50051"
kIP = 'localhost'


class Sensors(str, Enum):
    KEY_TEMP = "TEMP"
    KEY_LUMI = "LUMI"
    KEY_SMOKE = "SMOKE"


class Server(pb_grpc.ACServicer):
    def __init__(self):
        pass

    def start_rpc(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb_grpc.add_ACServicer_to_server(
            ACService(), server)
        server.add_insecure_port("[::]:"+kPort)
        server.start()
        print("[RPC] Running!")
        server.wait_for_termination()

    def start_rabbit(self):

        print("[Rabbit] Running!")

        EXCHANGE_NAME = "EXCHANGE"

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(
            exchange=EXCHANGE_NAME, exchange_type='direct')
        channel.queue_declare(
            queue=Sensors.KEY_TEMP, arguments={'x-message-ttl': 1000}, exclusive=True)
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=Sensors.KEY_TEMP)

        print(' [Rabbit][*] Waiting for logs. To exit press CTRL+C')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=Sensors.KEY_TEMP, on_message_callback=self.callback, auto_ack=True)

        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        message = body.decode('utf8').split("-")
        actuator = message[0]
        content = message[1]

        channel = grpc.insecure_channel(kIP+':'+kPort)

        match actuator:
            case Sensors.KEY_TEMP:
                stub = pb_grpc.ACStub(channel)
                if float(content) > 30:
                    try:
                        resp = stub.changeTemperature(
                            pb.TempRequest(tempCelsius=25.0))
                        print(
                            f"Temperature changed to {resp.tempCelsius} ")

                    except Exception as err:
                        print(err)
                elif float(content) < 20:
                    resp = stub.switchPower(pb.Empty())
                    print(
                        f"Power Status: {resp.status} ")

            case Sensors.KEY_SMOKE:
                pass
            case Sensors.KEY_LUMI:
                pass

        print(f"{actuator} - {content}")

    def run(self):
        rabbit_thread = threading.Thread(
            target=self.start_rabbit)
        rabbit_thread.start()
        self.start_rpc()


if __name__ == "__main__":
    server = Server()
    server.run()
