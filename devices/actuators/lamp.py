from enum import Enum
import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc
from devices.actuators.actuator import Actuator


class Color(str, Enum):

    WHITE = "WHITE"
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    ORANGE = "ORANGE"
    PURPLE = "PURPLE"
    BROWN = "BROWN"


class Lamp(Actuator, pb_grpc.LampServicer):
    def __init__(self):
        super().__init__()
        self.power = False
        self.color = Color.WHITE

    def changeColor(self, request, context):
        self.color = request.color
        return pb.ColorResponse(color=self.color)
