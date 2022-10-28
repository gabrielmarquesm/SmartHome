from concurrent import futures
import threading
import time

import grpc
import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc

from devices.actuators.AC import AC
from devices.actuators.alarm import Alarm
from devices.actuators.lamp import Lamp
from devices.sensors.motion import Motion
from devices.sensors.sound import Sound
from devices.sensors.temperature import Temperature

from utils import kPort


def start_rpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_ACServicer_to_server(
        AC(), server)
    pb_grpc.add_LampServicer_to_server(
        Lamp(), server)
    pb_grpc.add_AlarmServicer_to_server(
        Alarm(), server)
    server.add_insecure_port("[::]:"+kPort)
    server.start()
    print("[RPC] Running!")
    server.wait_for_termination()


def start_sensors():
    #sleep_time = 5
    Temperature("TEMP")
    Motion("MOTION")
    Sound("SOUND")


if __name__ == "__main__":
    sensors_thread = threading.Thread(
        target=start_sensors)

    sensors_thread.start()
    start_rpc()
