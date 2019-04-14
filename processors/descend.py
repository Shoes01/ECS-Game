import esper

from components.actor.descend import DescendComponent
from components.game.events import EventsComponent
from components.stairs import StairsComponent
from components.position import PositionComponent

class DescendProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (des, pos) in self.world.get_components(DescendComponent, PositionComponent):
            # Look to see if we are standing on stairs.
            for stairs, (s_pos, _) in self.world.get_components(PositionComponent, StairsComponent):
                if pos.x == s_pos.x and pos.y == s_pos.y:
                    self.world.add_component(1, EventsComponent(events=[{'new_map': True}]))
                    break
            else:
                self.world.remove_component(ent, DescendComponent)