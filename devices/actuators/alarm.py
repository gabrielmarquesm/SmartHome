import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc
from devices.actuators.actuator import Actuator


class Alarm(Actuator, pb_grpc.AlarmServicer):
    def __init__(self):
        super().__init__()

    def sendMessage(self, request, context):
        message_ = "Someone is in the house, Police is already on the way!"
        return pb.MessageResponse(message=message_)
