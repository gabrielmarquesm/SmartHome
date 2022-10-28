from concurrent import futures
import threading
import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc
import grpc
from home_assistant import HomeAssistant
from utils import kPort, kIP, Sensors, kPortClient


class Client():

    def show_menu(self):
        channel = grpc.insecure_channel(kIP+':'+kPortClient)
        stub = pb_grpc.HomeAssistantStub(channel)
        while True:
            print("Sensors: ")
            print(f"1 - {Sensors.MOTION} ")
            print(f"2 - {Sensors.TEMP} ")
            print(f"3 - {Sensors.SOUND} ")
            sensor = input("Select Sensor: ")

            response = stub.checkSensorInfo(pb.Key(key=sensor)).info
            print(f"Response: {response}")

            # match sensor:
            #     case Sensors.TEMP:
            #         pass
            #     case Sensors.SOUND:
            #         pass
            #     case Sensors.MOTION:
            #         pass

    def run(self):

        menu_thread = threading.Thread(
            target=self.show_menu)
        menu_thread.start()


if __name__ == "__main__":
    client = Client()
    client.run()
