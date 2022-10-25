from enum import Enum

kPort = "50051"
kIP = 'localhost'
kExchange = "EXCHANGE"


class Sensors(str, Enum):
    TEMP = "TEMP"
    LUMI = "LUMI"
    SMOKE = "SMOKE"
