import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc
from devices.actuators.actuator import Actuator


class AC(Actuator, pb_grpc.ACServicer):
    def __init__(self):
        super().__init__()
        self.temperature = 25.0

    def changeTemperature(self, request, context):
        self.temperature = request.tempCelsius
        return pb.TempResponse(tempCelsius=self.temperature)
