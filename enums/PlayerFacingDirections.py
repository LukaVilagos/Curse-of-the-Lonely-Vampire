from enum import Enum
from utils.pg import pg

class PlyerFacingDirections(Enum):
    UP = pg.math.Vector2(0, -1)
    DOWN = pg.math.Vector2(0, 1)
    LEFT = pg.math.Vector2(-1, 0)
    RIGHT = pg.math.Vector2(1, 0)
    