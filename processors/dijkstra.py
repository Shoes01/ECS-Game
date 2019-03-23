import esper
import numpy as np

from _helper_functions import tile_occupied
from collections import deque
from components.actor.actor import ActorComponent
from components.position import PositionComponent
from processors.ai_input import AiInputProcessor
from processors.debug import DebugProcessor

class DijkstraProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.blank_dijkstra_map = [] # Injected via MapgenProcessor
        self.directory = [] # Injected via MapgenProcessor

    def process(self):
        if self.world.get_processor(AiInputProcessor):
            # Recalculate dijkstra map.
            dijkstra_map = self.blank_dijkstra_map
            player_pos = self.world.component_for_entity(2, PositionComponent)
            start = player_pos.x, player_pos.y
            frontier = deque()
            frontier.append(start)
            visited = {}
            visited[start] = True

            dijkstra_map[start[0], start[1]] = 0

            while len(frontier):
                current = frontier.popleft()

                for neighbor in self.directory[current]:
                    if neighbor not in visited:
                        if tile_occupied(self.world, neighbor[0], neighbor[1]):
                            dijkstra_map[neighbor[0], neighbor[1]] = dijkstra_map[current[0], current[1]] + 15
                            
                        else:
                            dijkstra_map[neighbor[0], neighbor[1]] = dijkstra_map[current[0], current[1]] + 1
                        
                            if not dijkstra_map[neighbor[0], neighbor[1]] > 20: # Cheap optimization.
                                frontier.append(neighbor)
                        
                        visited[neighbor] = True
            
            self.world.get_processor(AiInputProcessor).dijkstra_map = dijkstra_map
            self.world.get_processor(AiInputProcessor).directory = self.directory
            if self.world.get_processor(DebugProcessor):
                self.world.get_processor(DebugProcessor).dijkstra_map = dijkstra_map