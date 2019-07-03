from _data import ENTITY_COLORS, MULTIPLIER
from components.actor.actor import ActorComponent
from components.actor.corpse import CorpseComponent
from components.item.item import ItemComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.stairs import StairsComponent
from components.tile import TileComponent

def render_entities(console_object, recompute_fov, world):
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

    console, x, y, w, h = console_object

    # Sort them into lists.
    for ent, (pos, ren) in world.get_components(PositionComponent, RenderComponent):
        # Prerender the entity
        if world.map.fov_map.fov[pos.x, pos.y]:
            ren.explored = True
            ren.visible = True
        else:
            ren.visible = False
        
        if ent == 1: continue

        if world.has_component(ent, StairsComponent):
            _sorted_list['stairs'].append((pos, ren))
        elif world.has_component(ent, TileComponent):
            _sorted_list['tile'].append((pos, ren))
        elif world.has_component(ent, CorpseComponent):
            _sorted_list['corpse'].append((pos, ren))
        elif world.has_component(ent, ItemComponent):
            _sorted_list['item'].append((pos, ren))
        elif world.has_component(ent, ActorComponent):
            _sorted_list['actor'].append((pos, ren))

    # Print tiles to the console.
    for (pos, ren) in _sorted_list.get('tile') or []:
        print_tile_special(console, pos, ren, _entity_directory, world)

    # Print corpses.
    for (pos, ren) in _sorted_list.get('corpse') or []:
        print_tile(console, pos, ren, _entity_directory)

    # Print items.
    for (pos, ren) in _sorted_list.get('item') or []:
        print_tile(console, pos, ren, _entity_directory)

    # Print stairs.
    for (pos, ren) in _sorted_list.get('stairs') or []:
        print_tile(console, pos, ren, _entity_directory)

    # Print entities.
    for (pos, ren) in _sorted_list.get('actor') or []:
        print_tile(console, pos, ren, _entity_directory)
    
    # Print the player (again), on top of everything else.
    player_pos = world.component_for_entity(1, PositionComponent)
    player_ren = world.component_for_entity(1, RenderComponent)
    if not world.has_component(1, CorpseComponent):
        print_tile(console, player_pos, player_ren, _entity_directory)
    
    # Print cursor.
    cursor = world.cursor
    if world.state == 'Look':
        console.print(cursor.x, cursor.y, cursor.char, cursor.color)

def print_tile_special(console, pos, ren, _entity_directory, world):
    x, y = pos.x*2, pos.y*2
    fg = ren.color + (255,)
    bg = ren.bg_color + (255,)
    multiplier = MULTIPLIER
    
    if world.state is not 'SkillTargeting':
        ren.highlight_color = None
    
    if ren.visible or ren.explored:
        if ren.explored and not ren.visible:
            bg = (0, 0, 0, 0)
        
        if ren.highlight_color:
            bg = ren.highlight_color + (255,)
        
        iter = 0
        for yy in range(0, multiplier):
            for xx in range(0, multiplier):
                console.tiles["ch"][x + xx, y + yy] = ord(u'\U000F0000') + ren.codepoint*multiplier*multiplier + iter
                console.tiles["fg"][x + xx, y + yy] = fg
                console.tiles["bg"][x + xx, y + yy] = bg
                iter += 1

def print_tile(console, pos, ren, _entity_directory):
    x, y = pos.x*2, pos.y*2
    fg = ren.color + (255,)
    bg = ren.bg_color + (255,)
    multiplier = MULTIPLIER
    
    if (pos.x, pos.y) not in _entity_directory:
        _entity_directory.append((pos.x, pos.y))
    else:
        bg = ENTITY_COLORS['overlap_bg'] + (255,)

    if ren.visible:        
        iter = 0
        for yy in range(0, multiplier):
            for xx in range(0, multiplier):
                console.tiles["ch"][x + xx, y + yy] = ord(u'\U000F0000') + ren.codepoint*multiplier*multiplier + iter
                console.tiles["fg"][x + xx, y + yy] = fg
                console.tiles["bg"][x + xx, y + yy] = bg
                iter += 1