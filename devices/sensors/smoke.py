from devices.sensors.sensor import Sensor


class Smoke(Sensor):
    def __init__(self, key):
        super().__init__(key)

    def calculate(self):
        pass

    def get_info(self):
        pass