from components.game.map import MapComponent
from components.position import PositionComponent
from components.render import RenderComponent

def process_prerender(world):
    game_map = world.component_for_entity(1, MapComponent)

    if game_map.fov_map:
        pos_player = world.component_for_entity(2, PositionComponent)
        game_map.fov_map.compute_fov(x=pos_player.x, y=pos_player.y, radius=10, light_walls=True, algorithm=0)

        for ent, (pos, ren) in world.get_components(PositionComponent, RenderComponent):
            if game_map.fov_map.fov[pos.x, pos.y]:
                ren.explored = True
                ren.visible = True
            else:
                ren.visible = False