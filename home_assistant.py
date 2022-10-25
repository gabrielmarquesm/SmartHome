from concurrent import futures
import threading

import grpc
from grpc import Status
import pika

import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc
from devices.actuators.AC import ACService, StatusMessageAC
from utils import kIP, kPort, Sensors, kExchange


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

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=kIP))
        channel = connection.channel()
        channel.exchange_declare(
            exchange=kExchange, exchange_type='direct')
        channel.queue_declare(
            queue=Sensors.TEMP, arguments={'x-message-ttl': 1000}, exclusive=True)
        channel.queue_bind(exchange=kExchange, queue=Sensors.TEMP)

        print(' [Rabbit][*] Waiting for logs. To exit press CTRL+C')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=Sensors.TEMP, on_message_callback=self.callback, auto_ack=True)

        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        message = body.decode('utf8').split("-")
        actuator = message[0]
        content = message[1]

        channel = grpc.insecure_channel(kIP+':'+kPort)

        match actuator:
            case Sensors.TEMP:
                temp = float(content)
                stub = pb_grpc.ACStub(channel)
                self.temp_handler(temp, stub)

            case Sensors.SMOKE:
                pass
                # smoke_density = float(content)
                # stub = pb_grpc.SmokeStub(channel)
                # self.smoke_handler(temp, stub)
            case Sensors.LUMI:
                # lumix = float(content)
                # stub = pb_grpc.LumiStub(channel)
                # self.luminosity_handler(temp, stub)
                pass

    def run(self):
        rabbit_thread = threading.Thread(
            target=self.start_rabbit)
        rabbit_thread.start()
        self.start_rpc()

    def temp_handler(self, temp, stub):
        if temp > 30:
            status = stub.turnOn(pb.Empty()).status
            print(f"\nAmbient Temperature is too high - {temp} °C")
            if status == StatusMessageAC.ON:
                print("Turning ON AC...")
            elif status == StatusMessageAC.ALREADY_ON:
                status = stub.changeTemperature(
                    pb.TempRequest(tempCelsius=18.0))
                print(
                    f"Cooling Mode - Changing temp to {status.tempCelsius} °C\n")

        elif temp < 15:
            status = stub.turnOn(pb.Empty()).status
            print(f"\nAmbient Temperature is too low - {temp} °C")
            if status == StatusMessageAC.ON:
                print("Turning ON AC...")
            elif status == StatusMessageAC.ALREADY_ON:
                status = stub.changeTemperature(
                    pb.TempRequest(tempCelsius=27.0))
                print(
                    f"Warming Mode - Changing temp to {status.tempCelsius} °C\n")

        elif 15 <= temp <= 20:
            status = stub.turnOff(pb.Empty()).status
            print(f"\nAmbient Temperature is OK - {temp} °C")
            if status == StatusMessageAC.OFF:
                print("Turning OFF AC...")

    def smoke_handler(self, smoke_density, stub):
        pass

    def luminosity_handler(self, lux, stub):
        pass


if __name__ == "__main__":
    server = Server()
    server.run()
