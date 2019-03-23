import esper
import random

from components.action import ActionComponent
from components.actor.actor import ActorComponent
from components.actor.brain import BrainComponent
from components.actor.has_turn import HasTurnComponent
from components.game.map import MapComponent
from components.position import PositionComponent
from components.player import PlayerComponent

class AiInputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        if not self.world.has_component(2, HasTurnComponent):
            for ent, (actor, brain, pos) in self.world.get_components(ActorComponent, BrainComponent, PositionComponent):
                if brain.brain == 'zombie':
                    self.take_turn_zombie( brain, ent, pos)
                    self.world.add_component(ent, HasTurnComponent())
            
            self.world.add_component(2, HasTurnComponent())
            self.world.remove_processor(AiInputProcessor)
    
    def take_turn_zombie(self, brain, ent, pos):
        if brain.awake is False and LOS(pos, self.world.component_for_entity(2, PositionComponent)):
            brain.awake = True
            return
    
        action = self.hunt_player(pos)
        self.world.add_component(ent, ActionComponent(action))
                
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

        return {'move': best_direction}

def LOS(pos1, pos2):
    return True