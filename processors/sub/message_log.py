import tcod as libtcod

from _data import LOG_COLORS
from components.game.message_log import MessageLogComponent

def render_message_log(console_bundle, world):
    message_log = world.component_for_entity(1, MessageLogComponent).messages
    console, x, y, w, h = console_bundle

    dy = h - 1
    for message in reversed(message_log):
        _combat = message.get('combat')
        _consume_fail = message.get('consume_fail')
        _consume_generic = message.get('consume_generic')
        _death = message.get('death')
        _error = message.get('error')
        _heal = message.get('heal')
        _max_hp = message.get('max_hp')

        if _combat:
            att_char, att_color, def_char, def_color, damage, turn = _combat

            libtcod.console_set_color_control(libtcod.COLCTRL_1, att_color, libtcod.black)
            libtcod.console_set_color_control(libtcod.COLCTRL_2, def_color, libtcod.black)
            console.print(0, 0 + dy, '(Turn %s) %c%s%c hits %c%s%c for %s.' % (turn, libtcod.COLCTRL_1, att_char, libtcod.COLCTRL_STOP, libtcod.COLCTRL_2, def_char, libtcod.COLCTRL_STOP, damage), LOG_COLORS['combat'])

        if _consume_fail:
            name, turn = _consume_fail

            console.print(0, 0 + dy, '(Turn %s) You cannot consume your %s!' % (turn, name), LOG_COLORS['consume_generic'])

        if _consume_generic:
            name, turn = _consume_generic

            console.print(0, 0 + dy, '(Turn %s) You consume your %s.' % (turn, name), LOG_COLORS['consume_generic'])

        if _death:
            char, color, turn = _death

            libtcod.console_set_color_control(libtcod.COLCTRL_1, color, libtcod.black)
            console.print(0, 0 + dy, '(Turn %s) The %c%s%c has died!' % (turn, libtcod.COLCTRL_1, char, libtcod.COLCTRL_STOP), LOG_COLORS['death'])
        
        if _error:
            message= _error

            console.print(0, 0 + dy, message, LOG_COLORS['error'])
        
        if _heal:
            value, turn = _heal

            console.print(0, 0 + dy, '(Turn %s) You heal for %s point(s).' % (turn, value), LOG_COLORS['heal'])
        
        if _max_hp:
            value, turn = _max_hp

            console.print(0, 0 + dy, '(Turn %s) Your max hp increases by %s point(s).' % (turn, value), LOG_COLORS['max_hp'])

        dy -= 1
        if dy < 0:
            break