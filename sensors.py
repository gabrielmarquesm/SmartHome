import time
from devices.sensors.motion import Motion
from devices.sensors.sound import Sound
from devices.sensors.temperature import Temperature


if __name__ == "__main__":
    sleep_time = 15

    temp_ = Temperature("TEMP")
    time.sleep(sleep_time)

    motion_ = Motion("MOTION")
    time.sleep(sleep_time)

    sound_ = Sound("SOUND")

