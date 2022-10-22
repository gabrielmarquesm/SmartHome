import grpc

import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc

kPort = '50051'
kIP = 'localhost'


class TempClient(object):
    def __init__(self):
        pass

    def __create_request(self, temp):
        return pb.TempRequest(tempCelsius=temp)

    # def __create_stream_requests(self, num_reqs):
    #     requests = [self.__create_request(
    #         random.randint(20, 40)) for i in range(0, num_reqs)]

    #     for req in requests:
    #         print("Sent TempRequest[tempFahrenheit=%f]" % req.tempFahrenheit)
    #         yield req

    def run(self):
        channel = grpc.insecure_channel(kIP+':'+kPort)
        stub = pb_grpc.ACStub(channel)

        try:
            # temp = random.randint(20, 40)
            # req = self.__create_request(temp)

            # print("Sent change temp to %f" %
            #         req.tempCelsius)
            # resp = stub.changeTemperature(req)
            # print(
            #     "Received TempResponse[tempCelsius=%f]" % resp.tempCelsius)

            resp = stub.switchPower(pb.Empty())
            print(
                f"Received Power Status: {resp.status} ")
        except Exception as err:
            print(err)


if __name__ == '__main__':
    client = TempClient()
    client.run()
