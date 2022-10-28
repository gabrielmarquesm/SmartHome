from enum import Enum

kPort = "50051"
kPortClient = "3000"
kIP = 'localhost'
kExchange = "EXCHANGE"


class Sensors(str, Enum):
    TEMP = "TEMP"
    MOTION = "MOTION"
    SOUND = "SOUND"
