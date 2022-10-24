import random
import time
import threading

from devices.sensors.sensor import Sensor
from home_assistant import Sensors

kMinValue = 10.0
kMaxValue = 37.0
kInitialTemperature = 20.0


class Temperature(Sensor):
    def __init__(self, key):
        super().__init__(key)
        self.temp = kInitialTemperature
        self.publisher = threading.Thread(
            target=self.publish, args=[key])
        self.publisher.start()

    def calculate(self):
        value = random.uniform(kMinValue, kMaxValue)
        self.temp = round(value, 1)

    def get_info(self):
        # return {'Temperature' : self.temp}
        return f"{Sensors.KEY_TEMP}-{self.temp}"

    def publish(self, key):
        while True:
            self.calculate()
            self.channel.basic_publish(
                exchange=self.exchange_name, routing_key=key, body=self.get_info())
            print(f"Message sent: {self.get_info()}")
            time.sleep(5)
