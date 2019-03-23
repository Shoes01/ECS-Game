import cProfile
import time
import tcod as libtcod

from components.game.state import StateComponent
from processors.debug import DebugProcessor
from processors.input import InputProcessor
from world import build_world

def main():
    # Prepare console.
    libtcod.console_set_custom_font('rexpaint_cp437_10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)

    # Prepare input related objects.
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Prepare world. '1' is the game entity ID, '2' is the player ID.
    world = build_world()
 
    while True:
        # Handle input.
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        world.get_processor(InputProcessor).key = key
        world.get_processor(DebugProcessor).mouse = mouse

        # Do literally everything else.
        world.process()

        # Is there a way to exit the game from inside the processors?
        game_state = world.component_for_entity(1, StateComponent).state
        if game_state == 'Exit':
            return False

if __name__ == '__main__':
    # cProfile.run('main()') # This runs the profiler
    main()