from enum import Enum
import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc


class StatusMessageAC(str, Enum):
    ON = "ON"
    OFF = "OFF"
    ALREADY_ON = "Already ON"
    ALREADY_OFF = "Already OFF"


class ACService(pb_grpc.ACServicer):
    def __init__(self):
        self.power = True
        self.temperature = 25.0

    def turnOn(self, request, context):
        msg = ""
        if not self.power:
            self.power = True
            msg = StatusMessageAC.ON
        else:
            msg = StatusMessageAC.ALREADY_ON
        return pb.TempPowerStatus(status=msg)

    def turnOff(self, request, context):
        msg = ""
        if self.power:
            self.power = False
            msg = StatusMessageAC.OFF
        else:
            msg = StatusMessageAC.ALREADY_OFF
        return pb.TempPowerStatus(status=msg)

    # def switchPower(self, request, context):
    #     self.power = not (self.power)
    #     msg = "O ar-condicionado está desligado"
    #     if self.power:
    #         msg = "O ar-condicionado está ligado"
    #     return pb.TempPowerStatus(status=msg)

    def changeTemperature(self, request, context):
        self.temperature = request.tempCelsius
        return pb.TempResponse(tempCelsius=self.temperature)
