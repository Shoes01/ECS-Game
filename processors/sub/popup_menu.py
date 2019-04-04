import tcod as libtcod

from components.game.popup import PopupComponent

def render_popup_menu(console_bundle, world):
    if not world.has_component(1, PopupComponent):
        return

    console = console_bundle[0]
    popup_component = world.component_for_entity(1, PopupComponent)
    x, y, w, h = popup_component.x, popup_component.y, popup_component.w, popup_component.h
    
    console.draw_frame(x=x, y=y, width=w, height=h, title=popup_component.title, clear=True, fg=libtcod.white, bg=libtcod.black)

    # Render choices
    dy = 2
    for choice in popup_component.choices:
        name, key, _ = choice
        string = '(' + key + ') ' + name
        console.print(x + 2, y + dy, string, libtcod.white)
        dy += 1