from concurrent import futures
import json
import threading

import grpc
import pika

import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc
from devices.actuators.AC import AC
from devices.actuators.actuator import PowerStatus
from devices.actuators.alarm import Alarm
from devices.actuators.lamp import Lamp
from utils import convertColor, kIP, kPort, kPortClient, kExchange, Sensors, Actuators, Actions


class HomeAssistant():
    def __init__(self):
        self.sensors_info = {
            Sensors.TEMP: 25,
            Sensors.SOUND: 86,
            Sensors.MOTION: False
        }
        self.channel = grpc.insecure_channel(kIP+':'+kPort)

    def start_rpc_client(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb_grpc.add_HomeAssistantServicer_to_server(self, server)
        server.add_insecure_port("[::]:"+kPortClient)
        server.start()
        print("[RPC Client] Running!")
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
        self.create_queue(Sensors.SOUND, channel)

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

        match sensor:
            case Sensors.TEMP:
                temp: float = content
                self.sensors_info[Sensors.TEMP] = temp
                stub = pb_grpc.ACStub(self.channel)
                self.temp_handler(temp, stub)

            case Sensors.SOUND:
                db: int = content
                self.sensors_info[Sensors.SOUND] = db
                stub = pb_grpc.AlarmStub(self.channel)
                self.sound_handler(db, stub)

            case Sensors.MOTION:
                motion_detected: bool = content
                self.sensors_info[Sensors.MOTION] = motion_detected
                stub = pb_grpc.LampStub(self.channel)
                self.motion_handler(motion_detected, stub)

    def run(self):
        rabbit_thread = threading.Thread(
            target=self.start_rabbit)
        rabbit_thread.start()
        self.start_rpc_client()

    def temp_handler(self, temp, stub):
        if temp > 30:
            status = stub.turnOn(pb.Empty()).status
            print(f"[AC] Ambient Temperature is too high - {temp} °C")
            if status == PowerStatus.ON:
                print("[AC] Turning ON AC...")
            elif status == PowerStatus.ALREADY_ON:
                status = stub.changeTemperature(
                    pb.TempRequest(tempCelsius=18.0))
                print(
                    f"[AC] Cooling Mode - Set the AC to {status.tempCelsius} °C")

        elif temp < 15:
            status = stub.turnOn(pb.Empty()).status
            print(f"[AC] Ambient Temperature is too low - {temp} °C")
            if status == PowerStatus.ON:
                print("[AC] Turning ON AC...")
            elif status == PowerStatus.ALREADY_ON:
                status = stub.changeTemperature(
                    pb.TempRequest(tempCelsius=27.0))
                print(
                    f"[AC] Warming Mode - Set the AC to {status.tempCelsius} °C")

        elif 15 <= temp <= 20:
            status = stub.turnOff(pb.Empty()).status
            print(f"[AC] Ambient Temperature is OK - {temp} °C")
            if status == PowerStatus.OFF:
                print("[AC] Turning OFF AC...")

    def sound_handler(self, db, stub):
        if db > 100:
            print("[Alarm] Loud Sound Detected! ")
            stub.sendMessage(pb.Empty())

    def motion_handler(self, motion, stub):
        if motion:
            status = stub.turnOn(pb.Empty()).status

            if status == PowerStatus.ON:
                print("[Lamp] Motion Detected! Turning on Lamp...")
                stub.changeColor(pb.ColorRequest(color=pb.Color.RED))
                print("[Lamp] Lamp Color is now RED")

            elif status == PowerStatus.ALREADY_ON:
                print("[Lamp] Motion Detected but the lamp is already on")
                stub.changeColor(pb.ColorRequest(color=pb.Color.GREEN))
                print("[Lamp] Lamp Color is now GREEN")

    # Home Assistant functions
    def checkSensorInfo(self, request, context):
        key = request.key
        msg = str(self.sensors_info[key])
        return pb.Info(info=msg)

    def modifyActuator(self, request, context):
        match request.actuator:
            case Actuators.AC:
                stub = pb_grpc.ACStub(self.channel)
                temp = float(
                    request.param) if request.param.isnumeric() else 25.0
                match request.action:
                    case Actions.TURN_OFF:
                        return stub.turnOff(pb.Empty())
                    case Actions.TURN_ON:
                        return stub.turnOn(pb.Empty())
                    case Actions.CHANGE_TEMP:
                        response = stub.changeTemperature(
                            pb.TempRequest(tempCelsius=temp)).tempCelsius

                        return pb.Info(info=str(response))

            case Actuators.ALARM:
                stub = pb_grpc.AlarmStub(self.channel)
                match request.action:
                    case Actions.TURN_OFF:
                        return stub.turnOff(pb.Empty())
                    case Actions.TURN_ON:
                        return stub.turnOn(pb.Empty())

            case Actuators.LAMP:
                stub = pb_grpc.LampStub(self.channel)
                color = convertColor(request.param)
                match request.action:
                    case Actions.TURN_OFF:
                        return stub.turnOff(pb.Empty())
                    case Actions.TURN_ON:
                        return stub.turnOn(pb.Empty())
                    case Actions.CHANGE_COLOR:
                        color_id = stub.changeColor(
                            pb.ColorRequest(color=color)).color

                        return pb.Info(info=pb.Color.Name(color_id))


if __name__ == "__main__":
    server = HomeAssistant()
    server.run()
