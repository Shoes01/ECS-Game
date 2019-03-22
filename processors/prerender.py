import esper

from components.player import PlayerComponent
from components.position import PositionComponent
from components.render import RenderComponent

class PrerenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.fov_map = None
    
    def process(self):
        if self.fov_map:
            pos_player = self.world.component_for_entity(2, PositionComponent) # 2 is player
            self.fov_map.compute_fov(x=pos_player.x, y=pos_player.y, radius=10, light_walls=True, algorithm=0)

            for ent, (pos, ren) in self.world.get_components(PositionComponent, RenderComponent):
                if self.fov_map.fov[pos.x, pos.y]:
                    ren.explored = True
                    ren.visible = True
                else:
                    ren.visible = False