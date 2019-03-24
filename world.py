import esper
import tcod as libtcod

from processors.action import ActionProcessor
from processors.ai_input import AiInputProcessor
from processors.combat import CombatProcessor
from processors.debug import DebugProcessor
from processors.death import DeathProcessor
from processors.dijkstra import DijkstraProcessor
from processors.initial import InitialProcessor
from processors.input import InputProcessor
from processors.mapgen import MapgenProcessor
from processors.movement import MovementProcessor
from processors.prerender import PrerenderProcessor
from processors.render import RenderProcessor
from processors.state import StateProcessor

def build_world():
    # Create world.
    world = esper.World()

    # Instantiate Processors.
    action_processor = ActionProcessor()
    ai_input_processor = AiInputProcessor()
    combat_processor = CombatProcessor()
    debug_processor = DebugProcessor()
    death_processor = DeathProcessor()
    dijkstra_processor = DijkstraProcessor()
    initial_processor = InitialProcessor()
    input_processor = InputProcessor()
    mapgen_processor = MapgenProcessor()
    movement_processor = MovementProcessor()
    prerender_processor = PrerenderProcessor()
    render_processor = RenderProcessor()
    state_processor = StateProcessor()
    
    # Add them to the world.
    world.add_processor(initial_processor, 999)
    world.add_processor(state_processor, 70)
    world.add_processor(mapgen_processor, 60)
    world.add_processor(dijkstra_processor, 55)
    world.add_processor(prerender_processor, 50)
    world.add_processor(render_processor, 40)
    world.add_processor(debug_processor, 39)
    world.add_processor(ai_input_processor, 35)
    world.add_processor(input_processor, 30)
    world.add_processor(action_processor, 20)
    world.add_processor(movement_processor, 10)
    world.add_processor(combat_processor, 5)
    world.add_processor(death_processor, 1)

    return world