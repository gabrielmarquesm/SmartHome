from concurrent import futures
import grpc

import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc
from devices.actuators.AC import AC
from devices.actuators.alarm import Alarm
from devices.actuators.lamp import Lamp

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


if __name__ == "__main__":
    start_rpc()
