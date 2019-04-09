import tcod as libtcod

from _data import map
from components.game.popup import PopupComponent

def render_popup_menu(console_bundle, world):
    if not world.has_component(1, PopupComponent):
        return

    console = console_bundle[0]
    menus = world.component_for_entity(1, PopupComponent).menus 
    if not menus:
        return 0
    menu = menus[-1]
    x = 10
    y = 5
    w = map.w - 20
    h = map.h - 10
    
    console.draw_frame(x=x, y=y, width=w, height=h, title=menu[0], clear=True, fg=libtcod.white, bg=libtcod.black)

    # Render choices
    dy = 2
    for choice in menu[1]:
        name, key, _ = choice
        string = '(' + key + ') ' + name
        console.print(x + 2, y + dy, string, libtcod.white)
        dy += 1