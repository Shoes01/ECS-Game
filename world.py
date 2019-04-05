import esper
import tcod as libtcod

from processors.action import ActionProcessor
from processors.ai_input import AiInputProcessor
from processors.combat import CombatProcessor
from processors.debug import DebugProcessor
from processors.death import DeathProcessor
from processors.dijkstra import DijkstraProcessor
from processors.equip import EquipProcessor
from processors.event import EventProcessor
from processors.final import FinalProcessor
from processors.initial import InitialProcessor
from processors.input import InputProcessor
from processors.mapgen import MapgenProcessor
from processors.movement import MovementProcessor
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
    equip_processor = EquipProcessor()
    event_processor = EventProcessor()
    final_processor = FinalProcessor()
    initial_processor = InitialProcessor()
    input_processor = InputProcessor()
    mapgen_processor = MapgenProcessor()
    movement_processor = MovementProcessor()
    render_processor = RenderProcessor()
    state_processor = StateProcessor()
    
    # Add them to the world.
    ## UPKEEP
    world.add_processor(initial_processor, 999)
    ## RENDER
    world.add_processor(render_processor, 40)
    world.add_processor(debug_processor, 39)
    ## INPUT
    world.add_processor(ai_input_processor, 30)
    world.add_processor(input_processor, 30)
    ## UPDATE
    world.add_processor(action_processor, 20)
    world.add_processor(event_processor, 20)
    world.add_processor(equip_processor, 10)
    world.add_processor(movement_processor, 10)
    world.add_processor(combat_processor, 5)
    world.add_processor(death_processor, 4)
    world.add_processor(mapgen_processor, 3)
    world.add_processor(dijkstra_processor, 2)
    ## ENDSTEP
    world.add_processor(state_processor, 1)
    world.add_processor(final_processor, 0)

    return world