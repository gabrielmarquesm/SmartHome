from abc import ABC
from enum import Enum
import actuators_services_pb2 as pb


class PowerStatus(str, Enum):
    ON = "ON"
    OFF = "OFF"
    ALREADY_ON = "Already ON"
    ALREADY_OFF = "Already OFF"


class Actuator(ABC):
    def __init__(self):
        self.power = True

    def turnOn(self, request, context):
        msg = ""
        if not self.power:
            self.power = True
            msg = PowerStatus.ON
        else:
            msg = PowerStatus.ALREADY_ON
        return pb.PowerStatus(status=msg)

    def turnOff(self, request, context):
        msg = ""
        if self.power:
            self.power = False
            msg = PowerStatus.OFF
        else:
            msg = PowerStatus.ALREADY_OFF
        return pb.PowerStatus(status=msg)
