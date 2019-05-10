import tcod as libtcod

from _data import ENTITY_COLORS
from components.actor.actor import ActorComponent
from components.actor.corpse import CorpseComponent
from components.item.item import ItemComponent
from components.item.pickedup import PickedupComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.stairs import StairsComponent
from components.tile import TileComponent

def render_entities(world):
    if world.state == 'MainMenu' or world.state == 'PopupMenu':
        return 0
        
    prerender_entities(world)
    _entity_directory = []
    _ducpliates = []

    console, x, y, w, h = world.consoles['map']

    for ent, (pos, ren) in world.get_components(PositionComponent, RenderComponent):

        # Print tiles to the console.
        if world.has_component(ent, TileComponent):
            
            if world.state is not 'SkillTargeting':
                ren.highlight_color = None

            if ren.visible:
                if ren.highlight_color:
                    console.print(pos.x, pos.y, ren.char, fg=ren.color, bg=ren.highlight_color)
                else:
                    console.print(pos.x, pos.y, ren.char, ren.color)
            
            elif ren.explored:
                console.print(pos.x, pos.y, ren.char, ren.explored_color)

        # Print corpses.
        if world.has_component(ent, CorpseComponent):
            if ren.visible:
                console.print(pos.x, pos.y, ren.char, ren.color)

        # Print items.
        if world.has_component(ent, ItemComponent):
            if ren.visible and not world.has_component(ent, PickedupComponent):
                if (pos.x, pos.y) not in _entity_directory:
                    _entity_directory.append((pos.x, pos.y))
                    console.print(pos.x, pos.y, ren.char, ren.color)
                else:
                    console.print(pos.x, pos.y, ren.char, ren.color, ENTITY_COLORS['overlap_bg'])

        # Print stairs.
        if world.has_component(ent, StairsComponent):
            if ren.visible:
                if (pos.x, pos.y) not in _entity_directory:
                    _entity_directory.append((pos.x, pos.y))
                    console.print(pos.x, pos.y, ren.char, ren.color)
                else:
                    console.print(pos.x, pos.y, ren.char, ren.color, ENTITY_COLORS['overlap_bg'])

        # Print entities.
        if world.has_component(ent, ActorComponent):
            if ren.visible:
                if (pos.x, pos.y) not in _entity_directory:
                    _entity_directory.append((pos.x, pos.y))
                    console.print(pos.x, pos.y, ren.char, ren.color)
                else:
                    console.print(pos.x, pos.y, ren.char, ren.color, ENTITY_COLORS['overlap_bg'])

    # Print the player (again), on top of everything else.
    player_pos = world.component_for_entity(1, PositionComponent)
    player_ren = world.component_for_entity(1, RenderComponent)
    if not world.has_component(1, CorpseComponent):
        console.print(player_pos.x, player_pos.y, player_ren.char, player_ren.color)

    # Print cursor.
    cursor = world.cursor
    if cursor.active:
        console.print(cursor.x, cursor.y, cursor.char, cursor.color)

def prerender_entities(world):
    fov_map = world.map.fov_map

    if fov_map:
        pos_player = world.component_for_entity(1, PositionComponent)
        fov_map.compute_fov(x=pos_player.x, y=pos_player.y, radius=10, light_walls=True, algorithm=0)

        for ent, (pos, ren) in world.get_components(PositionComponent, RenderComponent):
            if fov_map.fov[pos.x, pos.y]:
                ren.explored = True
                ren.visible = True
            else:
                ren.visible = False