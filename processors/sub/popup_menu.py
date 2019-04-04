import tcod as libtcod

from components.game.popup import PopupComponent

def render_popup_menu(console_bundle, world):
    if not world.has_component(1, PopupComponent):
        return

    console, x, y, w, h = console_bundle
    popup_component = world.component_for_entity(1, PopupComponent)

    # Render the border
    for xx in range(popup_component.x, popup_component.x + popup_component.w):
        console.print(x + xx, y, '+', libtcod.white)
        console.print(x + w - 1 + xx, y, '+', libtcod.white)
    for yy in range(popup_component.y, popup_component.y + popup_component.h):
        console.print(x, y + yy, '+', libtcod.white)
        console.print(x, y + h - 1 + yy, '+', libtcod.white)
    
    # Render title
    console.print(x + 1, y + 1, popup_component.title, libtcod.white)

    # Render choices
    dy = 2
    for choice in popup_component.choices:
        name, key, result = choice
        console.print(x + 1, y + dy, name, libtcod.white)
        dy += 1
