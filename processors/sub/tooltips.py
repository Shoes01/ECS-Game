from _data import UI_COLORS
from _helper_functions import tile_has_items, tile_occupied
from components.actor.actor import ActorComponent
from components.game.cursor import CursorComponent
from components.game.input import InputComponent
from components.game.map import MapComponent
from components.item.item import ItemComponent
from components.name import NameComponent
from components.position import PositionComponent
from components.render import RenderComponent

def render_tooltips(console_bundle, world):
    console, _, _, _, h = console_bundle
    mouse_pos = world.component_for_entity(1, InputComponent).mouse_pos
    x, y = None, None
    
    if world.has_component(1, CursorComponent):
        cursor_pos = world.component_for_entity(1, CursorComponent)
        x, y = cursor_pos.x, cursor_pos.y
    elif mouse_pos:
        x, y = mouse_pos
        x -= 1
        y -= 1
    else:
        return 0

    _entity = None
    _found_items = False
    _items = "Items on the ground: "
    
    for ent, (name, pos, ren) in world.get_components(NameComponent, PositionComponent, RenderComponent):
        if ren.visible and pos.x == x and pos.y == y:
            if world.has_component(ent, ItemComponent):
                _found_items = True
                _items += name.name + ", "
            elif world.has_component(ent, ActorComponent):
                _entity = name.name

    _items = _items[:-2] + "."

    if _entity is not None:
        console.print(0, h - 1, _entity, UI_COLORS['text'])
        if _found_items:
            console.print(0, h - 2, _items, UI_COLORS['text'])
    elif _found_items:
        console.print(0, h - 1, _items, UI_COLORS['text'])