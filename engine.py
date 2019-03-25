import cProfile
import time
import tcod as libtcod

from _data import CONSOLE_HEIGHT, CONSOLE_WIDTH
from components.game.state import StateComponent
from processors.debug import DebugProcessor
from processors.input import InputProcessor
from processors.render import RenderProcessor
from world import build_world

def main():
    # Prepare console.
    libtcod.console_set_custom_font('rexpaint_cp437_10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)
    console = libtcod.console_init_root(CONSOLE_WIDTH, CONSOLE_HEIGHT, title='ECS Game', order='F')

    # Prepare input related objects.
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Prepare world. '1' is the game entity ID, '2' is the player ID.
    world = build_world()

    # Insert input and display related objects into certain processors.
    world.get_processor(DebugProcessor)._console = console
    world.get_processor(RenderProcessor)._console = console
 
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
        game_state = world.component_for_entity(1, StateComponent).state
        if game_state == 'Exit':
            return False

if __name__ == '__main__':
    # cProfile.run('main()') # This runs the profiler
    main()