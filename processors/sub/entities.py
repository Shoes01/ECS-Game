import tcod as libtcod

from _data import ENTITY_COLORS
from components.actor.actor import ActorComponent
from components.actor.corpse import CorpseComponent
from components.item.item import ItemComponent
from components.item.pickedup import PickedupComponent
from components.game.map import MapComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.stairs import StairsComponent
from components.tile import TileComponent

def render_entities(console_bundle, world):
    prerender_entities(world)
    _entity_directory = []
    _ducpliates = []

    console, x, y, w, h = console_bundle
    for ent, (pos, ren, tile) in world.get_components(PositionComponent, RenderComponent, TileComponent):
        
        if ren.visible:
            console.print(pos.x, pos.y, ren.char, ren.color)
        
        elif ren.explored:
            console.print(pos.x, pos.y, ren.char, ren.explored_color)            

    # Print corpses to the console.
    for ent, (corpse, pos, ren) in world.get_components(CorpseComponent, PositionComponent, RenderComponent):
        if ren.visible:
            console.print(pos.x, pos.y, ren.char, ren.color)

    # Print items.
    for ent, (item, pos, ren) in world.get_components(ItemComponent, PositionComponent, RenderComponent):
        if ren.visible and not world.has_component(ent, PickedupComponent):
            if (pos.x, pos.y) not in _entity_directory:
                _entity_directory.append((pos.x, pos.y))
                console.print(pos.x, pos.y, ren.char, ren.color)
            else:
                console.print(pos.x, pos.y, ren.char, ren.color, ENTITY_COLORS['overlap_bg'])

    # Print entities to the console.
    for ent, (actor, pos, ren) in world.get_components(ActorComponent, PositionComponent, RenderComponent):
        if ren.visible:
            if (pos.x, pos.y) not in _entity_directory:
                _entity_directory.append((pos.x, pos.y))
                console.print(pos.x, pos.y, ren.char, ren.color)
            else:
                console.print(pos.x, pos.y, ren.char, ren.color, ENTITY_COLORS['overlap_bg'])

    # Print stairs.
    for ent, (stairs, pos, ren) in world.get_components(StairsComponent, PositionComponent, RenderComponent):
        if ren.visible:
            if (pos.x, pos.y) not in _entity_directory:
                _entity_directory.append((pos.x, pos.y))
                console.print(pos.x, pos.y, ren.char, ren.color)
            else:
                console.print(pos.x, pos.y, ren.char, ren.color, ENTITY_COLORS['overlap_bg'])

    # Print the player (again), on top of everything else.
    player_pos = world.component_for_entity(2, PositionComponent)
    player_ren = world.component_for_entity(2, RenderComponent)
    if not world.has_component(2, CorpseComponent):
        console.print(player_pos.x, player_pos.y, player_ren.char, player_ren.color)

def prerender_entities(world):
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