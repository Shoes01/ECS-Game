import cProfile
import esper
import time
import tcod as libtcod

from components.position import Position
from components.render import Render
from components.velocity import Velocity
from input_handler import handle_keys
from processors.movement import MovementProcessor
from processors.render import RenderProcessor

def main():
    # Prepare console.
    libtcod.console_set_custom_font('rexpaint_cp437_10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)
    root = libtcod.console_init_root(80, 60, title='v0.0.0', order='F')

    # Prepare input related objects.
    game_state = 'Game'
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Prepare world.
    world = esper.World()

    # Instantiate Processors.
    movement_processor = MovementProcessor()
    render_processor = RenderProcessor(root)
    
    world.add_processor(render_processor, 100)
    world.add_processor(movement_processor, 50)

    # Create entities and assign them components.
    player = world.create_entity()
    world.add_component(player, Position(x=15, y=15))
    world.add_component(player, Velocity())
    world.add_component(player, Render('@', libtcod.white))

    try:
        while True:
            world.process()
            time.sleep(1)
    
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    # cProfile.run('main()') # This runs the profiler
    print("\nHeadless Example. Press Ctrl+C to quit!\n")
    main()