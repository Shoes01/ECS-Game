import esper
import tcod as libtcod

from processors.action import ActionProcessor
from processors.initial import InitialProcessor
from processors.input import InputProcessor
from processors.mapgen import MapgenProcessor
from processors.movement import MovementProcessor
from processors.prerender import PrerenderProcessor
from processors.render import RenderProcessor
from processors.state import StateProcessor

CONSOLE_HEIGHT = 60
CONSOLE_WIDTH = 80

def build_world():
    root = libtcod.console_init_root(CONSOLE_WIDTH, CONSOLE_HEIGHT, title='v0.0.0', order='F')

    # Create world.
    world = esper.World()

    # Instantiate Processors.
    action_processor = ActionProcessor()
    prerender_processor = PrerenderProcessor()
    initial_processor = InitialProcessor()
    input_processor = InputProcessor()
    mapgen_processor = MapgenProcessor(width=CONSOLE_WIDTH, height=CONSOLE_HEIGHT)
    movement_processor = MovementProcessor()
    render_processor = RenderProcessor(console=root)
    state_processor = StateProcessor()
    
    # Add them to the world.
    world.add_processor(initial_processor, 999)
    world.add_processor(state_processor, 70)
    world.add_processor(mapgen_processor, 60)
    world.add_processor(prerender_processor, 50)
    world.add_processor(render_processor, 40)
    world.add_processor(input_processor, 30)
    world.add_processor(action_processor, 20)
    world.add_processor(movement_processor, 10)

    return world