import cProfile
import time
import tcod as libtcod

from _data import con, eqp, log, map
from processors.debug import DebugProcessor
from processors.input import InputProcessor
from processors.render import RenderProcessor
from game import GameWorld

def main():
    # Prepare console.
    libtcod.console_set_custom_font('rexpaint_cp437_10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)
    consoles = {}
    consoles['con'] = (libtcod.console_init_root(con.w, con.h, title='ECS Game', order='F', renderer=libtcod.RENDERER_SDL2), con.x, con.y, con.w, con.h)
    consoles['stats'] = (libtcod.console.Console(eqp.w, eqp.h, order='F'), eqp.x, eqp.y, eqp.w, eqp.h)
    consoles['log'] = (libtcod.console.Console(log.w, log.h, order='F'), log.x, log.y, log.w, log.h)
    consoles['map'] = (libtcod.console.Console(map.w, map.h, order='F'), map.x, map.y, map.w, map.h)

    # Prepare world. '1' is the player ID.
    world = GameWorld()
    world.consoles = consoles
 
    while world.running:
        # Do literally everything.
        world.process()
    
    print('\n\n    Goodbye.\n')

if __name__ == '__main__':
    # cProfile.run('main()') # This runs the profiler
    main()