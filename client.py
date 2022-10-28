from concurrent import futures
import os
import threading
import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc
import grpc
from home_assistant import HomeAssistant
from utils import kPort, kIP, kPortClient, Sensors, Actuators, Actions


class Client():
    def __init__(self) -> None:
        self.channel = grpc.insecure_channel(kIP+':'+kPortClient)
        self.stub = pb_grpc.HomeAssistantStub(self.channel)

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def check_sensor(self, sensor_name):
        return self.stub.checkSensorInfo(pb.Key(key=sensor_name)).info

    def list_sensors(self):
        sensors = {
            Sensors.MOTION: self.check_sensor(Sensors.MOTION),
            Sensors.TEMP: self.check_sensor(Sensors.TEMP),
            Sensors.SOUND: self.check_sensor(Sensors.SOUND)
        }

        print("Sensors: ")
        print(
            f"Motion - {'Detected' if sensors[Sensors.MOTION] == 'True' else 'Undetected'}")
        print(f"Temperature - {sensors[Sensors.TEMP]} °C")
        print(f"Sound - {sensors[Sensors.SOUND]} DB")

    def modify_AC(self):
        print("1 - Turn On")
        print("2 - Turn Off")
        print("3 - Change Temperature")
        action = input("Select Action: ")
        msg = {
            'actuator': Actuators.AC,
            'action': None,
            'param': "0"
        }

        match action:
            case "1":
                msg["action"] = Actions.TURN_ON
                response = self.stub.modifyActuator(
                    pb.Params(actuator=msg["actuator"], action=msg["action"], param=msg["param"])).info
                print(response)
            case "2":
                msg["action"] = Actions.TURN_OFF
                response = self.stub.modifyActuator(
                    pb.Params(actuator=msg["actuator"], action=msg["action"], param=msg["param"])).info
                print(response)
            case "3":
                msg["action"] = Actions.CHANGE_TEMP
                msg["param"] = input("Enter a value in Celsius: ")
                response = self.stub.modifyActuator(
                    pb.Params(actuator=msg["actuator"], action=msg["action"], param=msg["param"])).info
                print(f"{response} °C")
            case other:
                print("No action found!")

    def modify_alarm(self):
        print("1 - Turn On")
        print("2 - Turn Off")
        action = input("Select Action: ")
        msg = {
            'actuator': Actuators.ALARM,
            'action': None,
            'param': "0"
        }
        match action:
            case "1":
                msg["action"] = Actions.TURN_ON
                response = self.stub.modifyActuator(
                    pb.Params(actuator=msg["actuator"], action=msg["action"], param=msg["param"])).info
                print(response)
            case "2":
                msg["action"] = Actions.TURN_OFF
                response = self.stub.modifyActuator(
                    pb.Params(actuator=msg["actuator"], action=msg["action"], param=msg["param"])).info
                print(response)
            case other:
                print("No action found!")

    def modify_lamp(self):
        print("1 - Turn On")
        print("2 - Turn Off")
        print("3 - Change Color")
        action = input("Select Action: ")
        msg = {
            'actuator': Actuators.LAMP,
            'action': None,
            'param': "0"
        }

        match action:
            case "1":
                msg["action"] = Actions.TURN_ON
                response = self.stub.modifyActuator(
                    pb.Params(actuator=msg["actuator"], action=msg["action"], param=msg["param"])).info
                print(response)
            case "2":
                msg["action"] = Actions.TURN_OFF
                response = self.stub.modifyActuator(
                    pb.Params(actuator=msg["actuator"], action=msg["action"], param=msg["param"])).info
                print(response)
            case "3":
                msg["action"] = Actions.CHANGE_COLOR
                msg["param"] = input("Enter a color name: ").upper()
                response = self.stub.modifyActuator(
                    pb.Params(actuator=msg["actuator"], action=msg["action"], param=msg["param"])).info
                print(response)
            case other:
                print("No action found!")

    def modify_actuator(self):
        print("Actuators: ")
        print("1 - AC")
        print("2 - Alarm")
        print("3 - Lamp")
        option = input("Select Actuator: ")
        self.clear_console()

        match option:
            case "1":
                self.modify_AC()
            case "2":
                self.modify_alarm()
            case "3":
                self.modify_lamp()
            case other:
                print("No option found!")

    def show_menu(self):
        while True:
            print("Home Assistant - Client")
            print("1 - Check Sensors information")
            print("2 - Choose Actuator")

            option = input("Select Option: ")
            self.clear_console()

            match option:
                case "1":
                    self.list_sensors()
                    input("Press ENTER to exit")
                    self.clear_console()
                case "2":
                    self.modify_actuator()
                case other:
                    print("No option found!")

    def run(self):
        menu_thread = threading.Thread(
            target=self.show_menu)
        menu_thread.start()


if __name__ == "__main__":
    client = Client()
    client.run()
