import esper
import numpy as np

from collections import deque
from components.actor.actor import ActorComponent
from components.position import PositionComponent

class DijkstraProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        if self.world.create_dijkstra_map:
            game_map = self.world.map
            player_pos = self.world.component_for_entity(1, PositionComponent)

            dijkstra_map = np.ones((game_map.width, game_map.height), dtype=int, order='F') * 999
            
            # Build dijkstra map.
            directory = game_map.directory
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
                        if self.world.get_entities_at(neighbor[0], neighbor[1], ActorComponent):
                            dijkstra_map[neighbor[0], neighbor[1]] = dijkstra_map[current[0], current[1]] + 15
                            
                        else:
                            dijkstra_map[neighbor[0], neighbor[1]] = dijkstra_map[current[0], current[1]] + 1
                        
                            if not dijkstra_map[neighbor[0], neighbor[1]] > 30: # Cheap optimization.
                                frontier.append(neighbor)
                        
                        visited[neighbor] = True

            # Push results to game entity.            
            game_map.dijkstra_map = dijkstra_map
            game_map.directory = directory

            self.world.create_dijkstra_map = False