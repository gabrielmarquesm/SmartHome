from enum import Enum
import actuators_services_pb2 as pb

kPort = "50051"
kPortClient = "3000"
kIP = 'localhost'
kExchange = "EXCHANGE"


class Color(str, Enum):

    WHITE = "WHITE"
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"


def convertColor(color):
    match color:
        case Color.WHITE:
            return pb.Color.WHITE
        case Color.RED:
            return pb.Color.RED
        case Color.GREEN:
            return pb.Color.GREEN
        case Color.BLUE:
            return pb.Color.BLUE
        case Color.YELLOW:
            return pb.Color.YELLOW
        case other:
            return pb.Color.WHITE


class Sensors(str, Enum):
    TEMP = "TEMP"
    MOTION = "MOTION"
    SOUND = "SOUND"


class Actuators(str, Enum):
    AC = "AC"
    ALARM = "ALARM"
    LAMP = "LAMP"


class Actions(str, Enum):
    TURN_ON = "TURN_ON"
    CHANGE_TEMP = "CHANGE_TEMP"
    TURN_OFF = "TURN_OFF"
    CHANGE_COLOR = "CHANGE_COLOR"
