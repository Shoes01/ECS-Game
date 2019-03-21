import esper

from components.player import Player
from components.position import Position
from components.render import Render

class PrerenderProcessor(esper.Processor):
    def __init__(self, fov_map):
        super().__init__()
        self.fov_map = fov_map
    
    def process(self):
        for ent_player, (player, pos_player) in self.world.get_components(Player, Position):
            self.fov_map.compute_fov(x=pos_player.x, y=pos_player.y, radius=10, light_walls=True, algorithm=0)

            for ent, (pos, ren) in self.world.get_components(Position, Render):
                if self.fov_map.fov[pos.x, pos.y]:
                    ren.explored = True
                    ren.visible = True
                else:
                    ren.visible = False