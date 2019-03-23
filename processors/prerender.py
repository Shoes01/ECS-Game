import esper

from components.game.map import MapComponent
from components.player import PlayerComponent
from components.position import PositionComponent
from components.render import RenderComponent

class PrerenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        game_map = self.world.component_for_entity(1, MapComponent)

        if game_map.fov_map:
            pos_player = self.world.component_for_entity(2, PositionComponent) # 2 is player
            game_map.fov_map.compute_fov(x=pos_player.x, y=pos_player.y, radius=10, light_walls=True, algorithm=0)

            for ent, (pos, ren) in self.world.get_components(PositionComponent, RenderComponent):
                if game_map.fov_map.fov[pos.x, pos.y]:
                    ren.explored = True
                    ren.visible = True
                else:
                    ren.visible = False