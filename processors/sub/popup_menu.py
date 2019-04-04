import tcod as libtcod

from components.game.popup import PopupComponent

def render_popup_menu(console_bundle, world):
    if not world.has_component(1, PopupComponent):
        return

    console = console_bundle[0]
    popup_component = world.component_for_entity(1, PopupComponent)
    x, y, w, h = popup_component.x, popup_component.y, popup_component.w, popup_component.h
    
    # Render the border
    for xx in range(x, x + w):
        console.print(xx, y, '+', libtcod.white)
        console.print(xx, y + h - 1, '+', libtcod.white)
    for yy in range(y, y + h):
        console.print(x, yy, '+', libtcod.white)
        console.print(x + w - 1, yy, '+', libtcod.white)
    
    # Render title
    console.print(x + 1, y + 1, popup_component.title, libtcod.white)

    # Render choices
    dy = 2
    for choice in popup_component.choices:
        name, key, _ = choice
        string = '(' + key + ') ' + name
        console.print(x + 2, y + dy, string, libtcod.white)
        dy += 1
