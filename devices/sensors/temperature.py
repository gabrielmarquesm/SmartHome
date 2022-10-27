from enum import Enum
import random
from devices.sensors.sensor import Sensor
from utils import Sensors


class TempBoundaries(float, Enum):
    INITIAL = 20.0
    MIN = 10.0
    MAX = 37.0


class Temperature(Sensor):
    def __init__(self, key):
        super().__init__(key)
        self.info = TempBoundaries.INITIAL

    def calculate(self):
        value = random.uniform(TempBoundaries.MIN, TempBoundaries.MAX)
        self.info = round(value, 1)

    def get_info(self):
        return {
            "sensor": Sensors.TEMP,
            "actuator": self.key,
            "content": self.info
        }
