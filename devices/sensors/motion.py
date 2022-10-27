import random
from devices.sensors.sensor import Sensor
from utils import Sensors


class Motion(Sensor):
    def __init__(self, key):
        super().__init__(key)
        self.info = False

    def calculate(self):
        self.info = random.choice([True, False])

    def get_info(self):
        return {
            "sensor": Sensors.MOTION,
            "actuator": self.key,
            "content": self.info
        }
