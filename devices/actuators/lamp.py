from enum import Enum

import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc
from devices.actuators.actuator import Actuator
from utils import Color


class Lamp(Actuator, pb_grpc.LampServicer):
    def __init__(self):
        super().__init__()
        self.power = False
        self.color = Color.WHITE

    def changeColor(self, request, context):
        if self.power:
            self.color = request.color
            return pb.ColorResponse(color=self.color)
        else:
            print("Lamp is not active")
