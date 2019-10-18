from _data import map, UI_COLORS

def render_popup_menu(console_object, world):
    console = console_object[0]
    menus = world.popup_menus
    if not menus:
        return 0

    menu = menus[-1]
    
    console.draw_frame(x=menu.x, y=menu.y, width=menu.w, height=menu.h, title=menu.title, clear=True, fg=UI_COLORS['fg'], bg=UI_COLORS['bg'])

    # Render choices
    dy = 2
    for choice in menu.contents:        
        color_fg = UI_COLORS['text']
        if not choice.valid:
            color_fg = UI_COLORS['text_invalid']

        string = '(' + choice.key + ') ' + choice.name.capitalize()
        console.print(menu.x + 2, menu.y + dy, string, color_fg)
        dy += 1
        if choice.description:
            console.print(menu.x + 2, menu.y + dy, "    " + choice.description, color_fg)
            dy += 1
        
        for condition in choice.conditions:
            color = color_fg
            if not condition.valid:
                color = UI_COLORS['text_condition_unmet']
            console.print(menu.x + 2, menu.y + dy, "    " + condition.description, color)
            dy += 1
    
    if menu.include_esc:
        console.print(menu.x + 2, menu.y + menu.h - 2, '(ESC) Close menu', UI_COLORS['text'])