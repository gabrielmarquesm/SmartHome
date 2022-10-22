from concurrent import futures

import grpc

import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc
from devices.actuators.AC import ACService

kPort = "50051"


class Server(pb_grpc.ACServicer):
    def __init__(self):
        pass

    # def to_celsius(self, tempFahrenheit):
    #     return (((tempFahrenheit - 32) * 5) / 9)

    # def convertReqResp(self, request, context):
    #     tempFahrenheit = request.tempFahrenheit
    #     print(f"Received tempRequest: {tempFahrenheit:.2f} F")
    #     tempCelsius = self.to_celsius(tempFahrenheit)
    #     print(f"Temperature in celsius: {tempCelsius:.2f} C")
    #     return pb.TempResponse(tempCelsius=tempCelsius)

    # def convertStream(self, response):
    #     pass

    def run(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb_grpc.add_ACServicer_to_server(
            ACService(), server)
        server.add_insecure_port("[::]:"+kPort)
        server.start()
        print("Server is Running!")
        server.wait_for_termination()


if __name__ == "__main__":
    server = Server()
    server.run()
