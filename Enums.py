import enum

class GameState(enum.Enum):
    ACTIVE = 0
    PLACE = 1

class CellType(enum.Enum):
    HOVER = (255, 255, 255)
    SELECT = (173, 216, 230)
    WATER = (0, 0, 255)
    SHIP = (100, 100, 100)
    SUNK = (0, 0, 0)

class ShipType(enum.Enum):
    AIRCRAFT_CARRIER = 5
    CRUISER = 4
    DESTROYER = 3
    FRIGATE = 3
    CORVETTE = 2

class Direction(enum.Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3