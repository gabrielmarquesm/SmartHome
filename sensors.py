from devices.sensors.motion import Motion
from devices.sensors.sound import Sound
from devices.sensors.temperature import Temperature


def start_sensors():
    #sleep_time = 5
    Temperature("TEMP")
    Motion("MOTION")
    Sound("SOUND")


if __name__ == "__main__":
    start_sensors()
