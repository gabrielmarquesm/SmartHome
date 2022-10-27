from enum import Enum

kPort = "50051"
kIP = 'localhost'
kExchange = "EXCHANGE"


class Sensors(str, Enum):
    TEMP = "TEMP"
    MOTION = "MOTION"
    SMOKE = "SMOKE"
