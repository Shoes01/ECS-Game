from data.render import UI_COLORS

def render_victory_screen(console_object):
    _string = 'You have won! Press ESC to return to the Main Menu.'
    console_object[0].print(3, 3, _string, UI_COLORS['text_mainmenu'])