import esper
import random

from components.actor.actor import ActorComponent
from components.actor.brain import BrainComponent
from components.actor.energy import EnergyComponent
from components.position import PositionComponent
from components.render import RenderComponent
from processors.movement import MovementProcessor
from processors.render import RenderProcessor
class AiInputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        _redraw = False
        for ent, (actor, brain, eng, pos, ren) in self.world.get_components(ActorComponent, BrainComponent, EnergyComponent, PositionComponent, RenderComponent):
            if eng.energy == 0:
                action = self.take_turn(brain, pos, ren)
                
                if action:
                    action['ent'] = ent
                    self.world.get_processor(action['processor']).queue.put(action)
                    _redraw = True
        
        self.world.get_processor(RenderProcessor).queue.put({'redraw': _redraw})
        
    def take_turn(self, brain, pos, ren):
        if brain.brain == 'zombie':
            if brain.awake is False and self.world.map.fov_map.fov[pos.x, pos.y]:
                brain.awake = True
                message = {'ai_awake': (ren.char, ren.color_fg, self.world.turn)}
                self.world.messages.append(message)
                return {'move': False, 'processor': MovementProcessor}

            elif brain.awake:                    
                return self.hunt_player(pos)
        
        return None
                
    def hunt_player(self, pos):
        x, y = pos.x, pos.y
        game_map = self.world.map
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

        return {'move': best_direction, 'processor': MovementProcessor}