import esper

from components.player import Player
from components.position import Position
from processors.render import RenderProcessor

class FovProcessor(esper.Processor):
    def __init__(self, fov_map):
        super().__init__()
        self.fov_map = fov_map
    
    def process(self):
        for ent, (player, pos) in self.world.get_components(Player, Position):
            self.fov_map.compute_fov(x=pos.x, y=pos.y, radius=10, light_walls=True, algorithm=0)

            self.world.get_processor(RenderProcessor).fov_map = self.fov_map