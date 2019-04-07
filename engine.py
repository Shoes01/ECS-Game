import cProfile
import time
import tcod as libtcod

from _data import con, eqp, log, map
from components.game.state import StateComponent
from processors.debug import DebugProcessor
from processors.input import InputProcessor
from processors.render import RenderProcessor
from world import build_world

def main():
    # Prepare console.
    libtcod.console_set_custom_font('rexpaint_cp437_10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)
    consoles = {}
    consoles['con'] = (libtcod.console_init_root(con.w, con.h, title='ECS Game', order='F'), con.x, con.y, con.w, con.h)
    consoles['stats'] = (libtcod.console.Console(eqp.w, eqp.h, order='F'), eqp.x, eqp.y, eqp.w, eqp.h)
    consoles['log'] = (libtcod.console.Console(log.w, log.h, order='F'), log.x, log.y, log.w, log.h)
    consoles['map'] = (libtcod.console.Console(map.w, map.h, order='F'), map.x, map.y, map.w, map.h)

    # Prepare input related objects.
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Prepare world. '1' is the game entity ID, '2' is the player ID.
    world = build_world()

    # Insert input and display related objects into certain processors.
    world.get_processor(DebugProcessor)._consoles = consoles
    world.get_processor(RenderProcessor)._consoles = consoles
 
    while True:
        # Handle input.
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        world.get_processor(DebugProcessor)._key = key
        world.get_processor(DebugProcessor)._mouse = mouse
        world.get_processor(InputProcessor)._key = key
        world.get_processor(InputProcessor)._mouse = mouse

        # Do literally everything else.
        world.process()

        # Is there a way to exit the game from inside the processors?
        if world._entities and world.component_for_entity(1, StateComponent).state == 'Exit':
            return False

if __name__ == '__main__':
    # cProfile.run('main()') # This runs the profiler
    main()