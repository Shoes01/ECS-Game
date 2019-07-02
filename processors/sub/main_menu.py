from _data import UI_COLORS

def render_main_menu(console_object):
    _string = 'Welcome to the Main Menu.\n\nPress ENTER to begin.\nPress L to load the last save.\n\nPress ESC to quit.'
    console_object[0].print(3, 3, _string, UI_COLORS['text_mainmenu'])