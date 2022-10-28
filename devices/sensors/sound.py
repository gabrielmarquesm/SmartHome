from enum import Enum
import random
from devices.sensors.sensor import Sensor
from utils import Sensors


class SoundBoundaries(float, Enum):
    INITIAL = 86
    MIN = 60
    MAX = 130


class Sound(Sensor):
    def __init__(self, key):
        super().__init__(key)
        self.info = SoundBoundaries.INITIAL

    def calculate(self):
        self.info = round(random.uniform(
            SoundBoundaries.MIN, SoundBoundaries.MAX))

    def get_info(self):
        return {
            "sensor": Sensors.SOUND,
            "actuator": self.key,
            "content": self.info
        }
