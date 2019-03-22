import esper
import random

from components.action import ActionComponent
from components.actor.actor import ActorComponent
from components.actor.brain import BrainComponent
from components.actor.has_turn import HasTurnComponent
from components.position import PositionComponent
from components.player import PlayerComponent

class AiInputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.dijkstra_map = []
    
    def process(self):
        for ent, (actor, brain, pos) in self.world.get_components(ActorComponent, BrainComponent, PositionComponent):
            if brain.brain == 'zombie':
                self.take_turn_zombie( brain, ent, pos)
                self.world.add_component(ent, HasTurnComponent())
        
        self.world.add_component(2, HasTurnComponent())
        self.world.remove_processor(AiInputProcessor)
    
    def take_turn_zombie(self, brain, ent, pos):
        if brain.awake is False and LOS(pos, self.world.component_for_entity(ent, PositionComponent)):
            brain.awake = True
            return
    
        action = self.hunt_player(pos)
        self.world.add_component(ent, ActionComponent(action))
                
    def hunt_player(self, pos):
        x, y = pos.x, pos.y
        lowest_value = self.dijkstra_map[y, x]
        directions = [(-1, 1), (1, -1), (1, 1), (-1, -1), (0, -1), (0, 1), (-1, 0), (1, 0)]
        best_direction = (0, 0)

        for direction in directions:
            new_value = self.dijkstra_map[y + direction[1], x + direction[0]]
            if new_value != 999 and new_value <= lowest_value:
                lowest_value = new_value
                best_direction = direction
                
        if best_direction == (0, 0):
            best_direction = random.choice(directions)

        return {'move': direction}

def LOS(pos1, pos2):
    return True