import tcod as libtcod

from _data import LOG_COLORS
from components.game.message_log import MessageLogComponent

def render_message_log(console_bundle, world):
    message_log = world.component_for_entity(1, MessageLogComponent).messages
    console, x, y, w, h = console_bundle

    dy = h - 1
    for message in message_log:
        # Print combat messages
        _combat = message.get('combat')
        _death = message.get('death')
        _error = message.get('error')

        if _combat:
            att_char, att_color, def_char, def_color, damage, turn = _combat

            libtcod.console_set_color_control(libtcod.COLCTRL_1, att_color, libtcod.black)
            libtcod.console_set_color_control(libtcod.COLCTRL_2, def_color, libtcod.black)
            console.print(0, 0 + dy, '(Turn %s) %c%s%c hits %c%s%c for %s.' % (turn, libtcod.COLCTRL_1, att_char, libtcod.COLCTRL_STOP, libtcod.COLCTRL_2, def_char, libtcod.COLCTRL_STOP, damage), LOG_COLORS['combat'])

        if _death:
            char, color, turn = _death

            libtcod.console_set_color_control(libtcod.COLCTRL_1, color, libtcod.black)
            console.print(0, 0 + dy, '(Turn %s) The %c%s%c has died!' % (turn, libtcod.COLCTRL_1, char, libtcod.COLCTRL_STOP), LOG_COLORS['death'])
        
        if _error:
            message= _error

            console.print(0, 0 + dy, message, LOG_COLORS['error'])

        dy -= 1
        if dy < 0:
            break