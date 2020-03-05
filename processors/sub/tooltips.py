from _data import MULTIPLIER
from components.actor.actor import ActorComponent
from components.item.item import ItemComponent
from components.name import NameComponent
from components.position import PositionComponent
from components.render import RenderComponent
from data.render import UI_COLORS
from fsm import Look

def render_tooltips(camera_pos, console_object, world):
    console, _, _, _, h = console_object
    cursor = world.cursor
    x, y = None, None
    
    if world.state == Look:
        x, y = cursor.x, cursor.y
    elif world.mouse_pos:
        x, y = world.mouse_pos
        x = (x-1) // MULTIPLIER + camera_pos[0]
        y = (y-1) // MULTIPLIER + camera_pos[1]
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
