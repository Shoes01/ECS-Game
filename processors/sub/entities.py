import tcod as libtcod

from _data import ENTITY_COLORS
from components.actor.actor import ActorComponent
from components.actor.corpse import CorpseComponent
from components.item.item import ItemComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.stairs import StairsComponent
from components.tile import TileComponent

def render_entities(world, recompute_fov):
    if world.state == 'MainMenu' or world.state == 'PopupMenu':
        return 0

    if recompute_fov:
        pos_player = world.component_for_entity(1, PositionComponent)
        world.map.fov_map.compute_fov(x=pos_player.x, y=pos_player.y, radius=10, light_walls=True, algorithm=0)

    _entity_directory = []
    _ducpliates = []
    _sorted_list = {
        'tile': [],
        'corpse': [],
        'item': [],
        'stairs': [],
        'actor': []
    }

    console, x, y, w, h = world.consoles['map']

    # Sort them into lists.
    for ent, (pos, ren) in world.get_components(PositionComponent, RenderComponent):
        # Prerender the entity
        if world.map.fov_map.fov[pos.x, pos.y]:
            ren.explored = True
            ren.visible = True
        else:
            ren.visible = False

        if world.has_component(ent, TileComponent):
            _sorted_list['tile'].append((pos, ren))
        elif world.has_component(ent, CorpseComponent):
            _sorted_list['corpse'].append((pos, ren))
        elif world.has_component(ent, ItemComponent):
            _sorted_list['item'].append((pos, ren))
        elif world.has_component(ent, StairsComponent):
            _sorted_list['stairs'].append((pos, ren))
        elif world.has_component(ent, ActorComponent):
            _sorted_list['actor'].append((pos, ren))

    # Print tiles to the console.
    for (pos, ren) in _sorted_list.get('tile') or []:
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
    for (pos, ren) in _sorted_list.get('corpse') or []:
        if ren.visible:
            console.print(pos.x, pos.y, ren.char, ren.color)

    # Print items.
    for (pos, ren) in _sorted_list.get('item') or []:
        if ren.visible:
            if (pos.x, pos.y) not in _entity_directory:
                _entity_directory.append((pos.x, pos.y))
                console.print(pos.x, pos.y, ren.char, ren.color)
            else:
                console.print(pos.x, pos.y, ren.char, ren.color, ENTITY_COLORS['overlap_bg'])

    # Print stairs.
    for (pos, ren) in _sorted_list.get('stairs') or []:
        if ren.visible:
            if (pos.x, pos.y) not in _entity_directory:
                _entity_directory.append((pos.x, pos.y))
                console.print(pos.x, pos.y, ren.char, ren.color)
            else:
                console.print(pos.x, pos.y, ren.char, ren.color, ENTITY_COLORS['overlap_bg'])

    # Print entities.
    for (pos, ren) in _sorted_list.get('actor') or []:
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
    if world.state == 'Look':
        console.print(cursor.x, cursor.y, cursor.char, cursor.color)