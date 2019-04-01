import esper
import tcod as libtcod

from _data import LOG_COLORS
from components.game.message_log import MessageLogComponent

class MessageLogProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self._consoles = {}

    def process(self):
        message_log = self.world.component_for_entity(1, MessageLogComponent).messages
        console, x, y, w, h = self._consoles['log'] # type: (console, x, y, w, h)

        console.clear()

        dy = h - 1
        for message in message_log:
            # Print combat messages
            _combat = message.get('combat')
            _death = message.get('death')

            if _combat:
                att_char, att_color, def_char, def_color, damage = _combat

                libtcod.console_set_color_control(libtcod.COLCTRL_1, att_color, libtcod.black)
                libtcod.console_set_color_control(libtcod.COLCTRL_2, def_color, libtcod.black)
                console.print(0, 0 + dy, ' %c%s%c hits %c%s%c for %s.' % (libtcod.COLCTRL_1, att_char, libtcod.COLCTRL_STOP, libtcod.COLCTRL_2, def_char, libtcod.COLCTRL_STOP, damage), LOG_COLORS['combat'])

            if _death:
                char, color = _death

                libtcod.console_set_color_control(libtcod.COLCTRL_1, color, libtcod.black)
                console.print(0, 0 + dy, ' The %c%s%c has died!' % (libtcod.COLCTRL_1, char, libtcod.COLCTRL_STOP), LOG_COLORS['death'])

            dy -= 1
        
        console.blit(dest=self._consoles['con'][0], dest_x=x, dest_y=y, src_x=0, src_y=0, width=w, height=h)