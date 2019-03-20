import cProfile
import time
import tcod as libtcod

from input_handler import handle_keys
from processors.input import InputProcessor
from world import build_world

def main():
    # Prepare console.
    libtcod.console_set_custom_font('rexpaint_cp437_10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)
    root = libtcod.console_init_root(80, 60, title='v0.0.0', order='F')

    # Prepare input related objects.
    game_state = 'Game'
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Prepare world.
    world = build_world(root)

    try:
        while True:
            # Handle input.
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
            world.get_processor(InputProcessor).action = handle_keys(game_state, key)
            
            # Do literally everything else.
            world.process()
    
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    # cProfile.run('main()') # This runs the profiler
    print("\nPress Ctrl+C to quit!\n")
    main()