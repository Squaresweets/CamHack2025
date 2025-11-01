@dataclass
class State:
    ready: List[int]
    clock_positions: List[Position]

@dataclass(frozen=True)
class Position:
    tile_x: int
    tile_y: int