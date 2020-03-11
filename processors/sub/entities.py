from _data import MULTIPLIER
from components.actor.actor import ActorComponent
from components.actor.corpse import CorpseComponent
from components.item.item import ItemComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.stairs import StairsComponent
from components.tile import TileComponent
from data.render import ENTITY_COLORS, SPRITES
from fsm import Look, SkillTargeting

def render_entities(console_object, world):
    _entity_directory = {}
    _ducpliates = []
    _sorted_list = {
        'tile': [],
        'corpse': [],
        'item': [],
        'stairs': [],
        'actor': [],
        'highlighted': []
    }

    console, _, _, _, _ = console_object

    # Sort them into lists.
    for ent, (pos, ren) in world.get_components(PositionComponent, RenderComponent):
        # Prerender the entity
        if world.map.fov_map.fov[pos.x, pos.y]:
            ren.visible = True
            if world.has_component(ent, TileComponent):
                ren.explored = True
        else:
            ren.visible = False
        
        if ent == 1: continue

        if world.has_component(ent, StairsComponent):
            _sorted_list['stairs'].append((pos, ren))
        elif world.has_component(ent, TileComponent):
            if world.state is SkillTargeting and ren.color_highlight:
                _sorted_list['highlighted'].append((pos, ren))
            _sorted_list['tile'].append((pos, ren))
        elif world.has_component(ent, CorpseComponent):
            _sorted_list['corpse'].append((pos, ren))
        elif world.has_component(ent, ItemComponent):
            _sorted_list['item'].append((pos, ren))
        elif world.has_component(ent, ActorComponent):
            _sorted_list['actor'].append((pos, ren))

    # Print tiles to the console.
    for (pos, ren) in _sorted_list.get('tile') or []:
        print_tile(console, pos, ren, _entity_directory, world, floor=True)

    # Print corpses.
    for (pos, ren) in _sorted_list.get('corpse') or []:
        print_tile(console, pos, ren, _entity_directory, world, corpse=True)

    # Print items.
    for (pos, ren) in _sorted_list.get('item') or []:
        print_tile(console, pos, ren, _entity_directory, world, items=True)

    # Print stairs.
    for (pos, ren) in _sorted_list.get('stairs') or []:
        print_tile(console, pos, ren, _entity_directory, world)

    # Print entities.
    for (pos, ren) in _sorted_list.get('actor') or []:
        print_tile(console, pos, ren, _entity_directory, world)
    
    # Print the player (again), on top of everything else.
    player_pos = world.component_for_entity(1, PositionComponent)
    player_ren = world.component_for_entity(1, RenderComponent)
    if not world.has_component(1, CorpseComponent):
        print_tile(console, player_pos, player_ren, _entity_directory, world)
    
    # Print the highlight cursors.
    for (pos, ren) in _sorted_list.get('highlighted') or []:
        print_cursor(ren.color_highlight, console, pos.x, pos.y, world)

    # Print cursor.
    cursor = world.cursor
    if world.state == Look:
        print_cursor(cursor.color_fg, console, cursor.x, cursor.y, world)

def print_cursor(color, console, x, y, world):
    cam_x, cam_y = world.camera.x, world.camera.y
    x, y = (x - cam_x)*MULTIPLIER, (y - cam_y)*MULTIPLIER
    codepoint = 790 # Reticle sprite.

    console.tiles["fg"][x : x + MULTIPLIER, y : y + MULTIPLIER] = color + (255,)
    console.tiles["bg"][x : x + MULTIPLIER, y : y + MULTIPLIER] = color + (0,)

    iter = 0
    for yy in range(0, MULTIPLIER):
        for xx in range(0, MULTIPLIER):
            console.tiles["ch"][x + xx, y + yy] = ord(u'\U000F0000') + codepoint*MULTIPLIER*MULTIPLIER + iter
            iter += 1

def print_tile(console, pos, ren, _entity_directory, world, corpse=False, floor=False, items=False):
    # Check to see that the tile is in the camera view.
    cam_x, cam_y, cam_w, cam_h = world.camera.x, world.camera.y, world.camera.w, world.camera.h
    if not (cam_x <= pos.x < cam_x + cam_w) or not (cam_y <= pos.y < cam_y + cam_h):
        return 0

    # Print tile.
    x, y = (pos.x - cam_x)*MULTIPLIER, (pos.y - cam_y)*MULTIPLIER
    codepoint = ren.codepoint
    fg = ren.color_fg + (255,)
    bg = ren.color_bg + (255,)
    
    if world.state is not SkillTargeting:
        ren.color_highlight = None
    
    if ren.visible or ren.explored:
        if ren.explored and not ren.visible:
            bg = ren.color_explored + (255,)
        
        if floor and ren.color_highlight:
            fg = ren.color_highlight + (255,)
            bg = (0, 0, 0, 0)
            codepoint = 790

        if not floor:
            if (x, y) in _entity_directory:
                new_bg = _entity_directory[(x, y)]
                if new_bg is not fg:
                    bg = new_bg
                if items:
                    fg = ENTITY_COLORS['loot_plural_fg'] + (255,)
                    codepoint = SPRITES['loot_plural']
            elif not corpse:
                _entity_directory[(x, y)] = fg

        console.tiles["fg"][x : x + MULTIPLIER, y : y + MULTIPLIER] = fg
        console.tiles["bg"][x : x + MULTIPLIER, y : y + MULTIPLIER] = bg
        
        iter = 0
        for yy in range(0, MULTIPLIER):
            for xx in range(0, MULTIPLIER):
                console.tiles["ch"][x + xx, y + yy] = ord(u'\U000F0000') + codepoint*MULTIPLIER*MULTIPLIER + iter
                iter += 1
