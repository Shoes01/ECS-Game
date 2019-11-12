import attr

from typing import Any, Dict, List, Tuple

@attr.s(auto_attribs=True)
class Map:
    ' The size of the playable area, including the dijkstra map used for pathfinding. '
    w: int
    h: int
    floor: int = 0
    dijkstra_map: Any = None # 2D numpy array
    directory: dict = Dict[Tuple[int, int], List[Tuple[int, int]]] # {coordinate: list of coordinates}
    fov_map: Any = None # Uhh... I think fov_maps is a 2D numpy array
    tiles: Any = None # 2D numpy array

    