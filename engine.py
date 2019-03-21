import cProfile
import time
import tcod as libtcod

from input_handler import handle_keys
from map import Map
from processors.input import InputProcessor
from world import build_world

def main():
    # Prepare console.
    libtcod.console_set_custom_font('rexpaint_cp437_10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)
    root = libtcod.console_init_root(80, 60, title='v0.0.0', order='F')

    # Prepare input related objects.
    key = libtcod.Key()
    game_map = Map(80, 60)
    mouse = libtcod.Mouse()

    # Prepare world.
    world = build_world(game_map, root) # 1: game entitiy. 2: player entity.
 
    while True:
        # Handle input.
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        action = handle_keys(key)
        
        if action.get('exit'):
            return False
        
        world.get_processor(InputProcessor).action = action
        
        # Do literally everything else.
        world.process()

if __name__ == '__main__':
    # cProfile.run('main()') # This runs the profiler
    main()