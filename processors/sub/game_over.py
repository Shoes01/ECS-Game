import tcod as libtcod

from _data import COLOR_THEME, UI_COLORS

def render_game_over(console_object):
    libtcod.console_set_color_control(libtcod.COLCTRL_1, COLOR_THEME['BrightRed'], COLOR_THEME['Red'])
    console_object[0].print(3, 3, 'You have %cDIED%c! Press ESC to return to the Main Menu.' % (libtcod.COLCTRL_1, libtcod.COLCTRL_STOP), UI_COLORS['text_mainmenu'], bg_blend=libtcod.BKGND_NONE)