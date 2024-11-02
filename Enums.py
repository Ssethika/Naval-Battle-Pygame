from enum import Enum
import enum

class GameState(enum.Enum):
    ACTIVE = 0
    PLACE = 1
    ATTACKING = 2

class CellType(enum.Enum):
    HOVER = (255, 255, 255)
    SELECT = (173, 216, 230)
    WATER = (0, 0, 255)
    SHIP = (100, 100, 100)
    SUNK = (0, 0, 0)

class ShipType(Enum):
    AIRCRAFT_CARRIER = 5
    CRUISER = 4
    DESTROYER = 3
    FRIGATE = 2
    CORVETTE = 1

ship_sizes = {
    ShipType.CORVETTE: 2,
    ShipType.FRIGATE: 3,
    ShipType.DESTROYER: 3,  # Same size as FRIGATE
    ShipType.CRUISER: 4,
    ShipType.AIRCRAFT_CARRIER: 5
}


class Direction(enum.Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

