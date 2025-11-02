from dataclasses import dataclass
from typing import List
from screens import *
@dataclass
class State:
    ready: List[int]
    clock_positions: List['Position']
    screen: Screen

@dataclass(frozen=True)
class Position:
    tile_x: int
    tile_y: int