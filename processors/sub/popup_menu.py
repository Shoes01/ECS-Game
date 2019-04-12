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
    
    console.draw_frame(x=menu.x, y=menu.y, width=menu.w, height=menu.h, title=menu.title, clear=True, fg=libtcod.white, bg=libtcod.black)

    # Render choices
    dy = 2
    for choice in menu.contents:        
        color = libtcod.white
        if not choice.valid:
            color = libtcod.grey

        string = '(' + choice.key + ') ' + choice.name
        console.print(menu.x + 2, menu.y + dy, string, color)
        dy += 1
    
    if menu.include_esc:
        console.print(menu.x + 2, menu.y + menu.h - 2, '(ESC) Close menu', libtcod.white)