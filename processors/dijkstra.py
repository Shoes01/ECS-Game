import esper
import numpy as np

from collections import deque
from components.actor.actor import ActorComponent
from components.position import PositionComponent
from processors.ai_input import AiInputProcessor
from processors.debug import DebugProcessor

class DijkstraProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.blank_dijkstra_map = []
        self.directory = []

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

            dijkstra_map[start[1], start[0]] = 0

            while len(frontier):
                current = frontier.popleft()

                for neighbor in self.directory[current]:
                    if neighbor not in visited:
                        if self.tile_occupied(neighbor[0], neighbor[1]):
                            dijkstra_map[neighbor[1], neighbor[0]] = dijkstra_map[current[1], current[0]] + 15
                            
                        else:
                            dijkstra_map[neighbor[1], neighbor[0]] = dijkstra_map[current[1], current[0]] + 1
                        
                            if not dijkstra_map[neighbor[1], neighbor[0]] > 20: # Cheap optimization.
                                frontier.append(neighbor)
                        
                        visited[neighbor] = True
            
            self.world.get_processor(AiInputProcessor).dijkstra_map = dijkstra_map
            if self.world.get_processor(DebugProcessor):
                self.world.get_processor(DebugProcessor).dijkstra_map = dijkstra_map

    
    def tile_occupied(self, x, y):
        for ent, (actor, pos) in self.world.get_components(ActorComponent, PositionComponent):
            if pos.x == x and pos.y == y:
                return True
        
        return False
