import esper
import random

from components.actor.action import ActionComponent
from components.actor.actor import ActorComponent
from components.actor.brain import BrainComponent
from components.actor.player import PlayerComponent
from components.actor.player_input import PlayerInputComponent
from components.game.map import MapComponent
from components.position import PositionComponent

class AiInputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        if not self.world.has_component(2, PlayerInputComponent):
            for ent, (actor, brain, pos) in self.world.get_components(ActorComponent, BrainComponent, PositionComponent):
                if brain.brain == 'zombie':
                    action = self.take_turn_zombie(brain, pos)
                    if action:
                        self.world.add_component(ent, ActionComponent(action))
            
            self.world.add_component(2, PlayerInputComponent())
    
    def take_turn_zombie(self, brain, pos):
        if brain.awake is False and self.world.component_for_entity(1, MapComponent).fov_map.fov[pos.x, pos.y]:
            brain.awake = True
        elif brain.awake:                    
            return self.hunt_player(pos)
        
        return None
                
    def hunt_player(self, pos):
        x, y = pos.x, pos.y
        game_map = self.world.component_for_entity(1, MapComponent)
        dijkstra_map = game_map.dijkstra_map
        directory = game_map.directory
        lowest_value = dijkstra_map[x, y]
        best_direction = (0, 0)

        for neighbour in directory[x, y]:
            new_value = dijkstra_map[neighbour[0], neighbour[1]]
            if new_value != 999 and new_value <= lowest_value:
                lowest_value = new_value
                best_direction = neighbour[0] - x, neighbour[1] - y

        if best_direction == (0, 0):
            neighbour = random.choice(directory[x, y])
            best_direction = neighbour[0] - x, neighbour[1] - y

        return {'move': best_direction}