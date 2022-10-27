from concurrent import futures
import json
import threading

import grpc
import pika

import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc
from devices.actuators.AC import AC
from devices.actuators.actuator import PowerStatus
from utils import kIP, kPort, Sensors, kExchange


class HomeAssistant():
    def __init__(self):
        pass

    def start_rpc(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb_grpc.add_ACServicer_to_server(
            AC(), server)
        server.add_insecure_port("[::]:"+kPort)
        server.start()
        print("[RPC] Running!")
        server.wait_for_termination()

    def start_rabbit(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=kIP))
        channel = connection.channel()
        channel.exchange_declare(
            exchange=kExchange, exchange_type='direct')
        channel.basic_qos(prefetch_count=1)

        self.create_queue(Sensors.TEMP, channel)
        self.create_queue(Sensors.MOTION, channel)

        print("[Rabbit] Running!")
        channel.start_consuming()

    def create_queue(self, name, channel):
        channel.queue_declare(
            queue=name, arguments={'x-message-ttl': 1000}, exclusive=True)
        channel.queue_bind(exchange=kExchange, queue=name)
        channel.basic_consume(
            queue=name, on_message_callback=self.callback, auto_ack=True)

    def callback(self, ch, method, properties, body):
        message = json.loads(body.decode('utf8'))

        sensor = message["sensor"]
        actuator = message["actuator"]
        content = message["content"]

        channel = grpc.insecure_channel(kIP+':'+kPort)

        match sensor:
            case Sensors.TEMP:
                temp: float = content
                stub = pb_grpc.ACStub(channel)
                self.temp_handler(temp, stub)

            case Sensors.SMOKE:
                pass
            case Sensors.MOTION:
                motion_detected: bool = content
                stub = pb_grpc.LampStub(channel)
                self.motion_handler(motion_detected, stub)

    def run(self):
        rabbit_thread = threading.Thread(
            target=self.start_rabbit)
        rabbit_thread.start()
        self.start_rpc()

    def temp_handler(self, temp, stub):
        if temp > 30:
            status = stub.turnOn(pb.Empty()).status
            print(f"\nAmbient Temperature is too high - {temp} °C")
            if status == PowerStatus.ON:
                print("Turning ON AC...")
            elif status == PowerStatus.ALREADY_ON:
                status = stub.changeTemperature(
                    pb.TempRequest(tempCelsius=18.0))
                print(
                    f"Cooling Mode - Changing temp to {status.tempCelsius} °C\n")

        elif temp < 15:
            status = stub.turnOn(pb.Empty()).status
            print(f"\nAmbient Temperature is too low - {temp} °C")
            if status == PowerStatus.ON:
                print("Turning ON AC...")
            elif status == PowerStatus.ALREADY_ON:
                status = stub.changeTemperature(
                    pb.TempRequest(tempCelsius=27.0))
                print(
                    f"Warming Mode - Changing temp to {status.tempCelsius} °C\n")

        elif 15 <= temp <= 20:
            status = stub.turnOff(pb.Empty()).status
            print(f"\nAmbient Temperature is OK - {temp} °C")
            if status == PowerStatus.OFF:
                print("Turning OFF AC...")

    def smoke_handler(self, smoke_density, stub):
        pass

    def motion_handler(self, motion, stub):

        if motion:
            status = stub.turnOn(pb.Empty()).status

            if status == PowerStatus.ON:
                print("Motion Detected! Turning on Lamp...")
                stub.changeColor(pb.ColorRequest(color=pb.Color.RED))
                print("Lamp Color is now RED")

            elif status == PowerStatus.ALREADY_ON:
                print("Motion Detected but the lamp is already on")
                stub.changeColor(pb.ColorRequest(color=pb.Color.GREEN))
                print("Lamp Color is now GREEN")


if __name__ == "__main__":
    server = HomeAssistant()
    server.run()
