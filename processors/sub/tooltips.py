from _data import UI_COLORS
from _helper_functions import tile_has_items, tile_occupied
from components.actor.actor import ActorComponent
from components.game.input import InputComponent
from components.game.map import MapComponent
from components.item.item import ItemComponent
from components.name import NameComponent
from components.position import PositionComponent
from components.render import RenderComponent

def render_tooltips(console_bundle, world):
    console, x, y, w, h = console_bundle
    mouse_pos = world.component_for_entity(1, InputComponent).mouse_pos
    mx, my = None, None
    if mouse_pos:
        mx, my = mouse_pos
        mx -= 1
        my -= 1
    else:
        return 0

    _entity = None
    _items = "Items on the ground: "
    _found_items = False
    
    for ent, (name, pos, ren) in world.get_components(NameComponent, PositionComponent, RenderComponent):
        if ren.visible and pos.x == mx and pos.y == my:
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

    


    """
    items = tile_has_items(world, mx, my)
    entity = tile_occupied(world, mx, my)

    _items = "Items on the ground: "
    for item in items:
        name = world.component_for_entity(item, NameComponent).name
        _items += name + ", "
    
    _items = _items[:-2] + "."
    
    _entity = None
    if entity:
        _entity = world.component_for_entity(entity, NameComponent).name

    if len(items) == 0 and _entity:
        console.print(0, h - 1, _entity, UI_COLORS['text'])
    """