import esper
import numpy as np

from _helper_functions import tile_occupied
from collections import deque
from components.actor.actor import ActorComponent
from components.game.dijgen import DijgenComponent
from components.game.map import MapComponent
from components.position import PositionComponent

class DijkstraProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        if self.world.has_component(1, DijgenComponent):
            # Calculate dijkstra map.
            game_map = self.world.component_for_entity(1, MapComponent)
            player_pos = self.world.component_for_entity(2, PositionComponent)

            dijkstra_map = np.ones((game_map.width, game_map.height), dtype=int, order='F') * 999

            # Build neighborhood.
            directory = {}
            directions = [(1, -1), (1, 1), (-1, -1), (-1, 1), (1, 0), (-1, 0), (0, -1), (0, 1)]
            
            for (x, y), _ in np.ndenumerate(game_map.tiles):
                results = []
                for direction in directions:
                    neighbor = (x + direction[0], y + direction[1])
                    if 0 <= neighbor[0] < game_map.width and 0 <= neighbor[1] < game_map.height and game_map.tiles[neighbor[0], neighbor[1]] == 0:
                        results.append(neighbor)
                
                directory[(x, y)] = results
            
            # Build dijkstra map.
            start = player_pos.x, player_pos.y
            frontier = deque()
            frontier.append(start)
            visited = {}
            visited[start] = True

            dijkstra_map[start[0], start[1]] = 0

            while len(frontier):
                current = frontier.popleft()

                for neighbor in directory[current]:
                    if neighbor not in visited:
                        if tile_occupied(self.world, neighbor[0], neighbor[1]):
                            dijkstra_map[neighbor[0], neighbor[1]] = dijkstra_map[current[0], current[1]] + 15
                            
                        else:
                            dijkstra_map[neighbor[0], neighbor[1]] = dijkstra_map[current[0], current[1]] + 1
                        
                            if not dijkstra_map[neighbor[0], neighbor[1]] > 30: # Cheap optimization.
                                frontier.append(neighbor)
                        
                        visited[neighbor] = True

            # Push results to game entity.            
            game_map.dijkstra_map = dijkstra_map
            game_map.directory = directory

            self.world.remove_component(1, DijgenComponent)