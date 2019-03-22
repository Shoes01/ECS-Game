import esper
import numpy as np
import tcod as libtcod

from components.actor import ActorComponent
from components.game.state import StateComponent
from components.player import PlayerComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.tile import TileComponent
from components.turn import TurnComponent
from components.velocity import VelocityComponent
from processors.action import ActionProcessor
from processors.input import InputProcessor
from processors.mapgen import MapgenProcessor
from processors.movement import MovementProcessor
from processors.prerender import PrerenderProcessor
from processors.render import RenderProcessor
from processors.state import StateProcessor

def build_world(game_map, root):
    world = esper.World()

    # Create game meta-entity.
    game = world.create_entity()
    world.add_component(game, StateComponent())

    # Create the player entity.
    player = world.create_entity()
    world.add_component(player, ActorComponent())
    world.add_component(player, PlayerComponent())
    world.add_component(player, PositionComponent(x=15, y=15))
    world.add_component(player, RenderComponent(char='@', color=libtcod.white))
    world.add_component(player, TurnComponent())
    world.add_component(player, VelocityComponent())

    ############==================== The stuff above will eventually be moved into either a game starting processor, or it's own little game starting function.

    # Instantiate Processors.
    action_processor = ActionProcessor()
    prerender_processor = PrerenderProcessor()
    input_processor = InputProcessor()
    level_processor = MapgenProcessor(height=game_map.height, tiles=game_map.tiles, width=game_map.width)
    movement_processor = MovementProcessor()
    render_processor = RenderProcessor(console=root)
    state_processor = StateProcessor()
    
    # Add them to the world.
    world.add_processor(state_processor, 70)
    world.add_processor(level_processor, 60)
    world.add_processor(prerender_processor, 50)
    world.add_processor(render_processor, 40)
    world.add_processor(input_processor, 30)
    world.add_processor(action_processor, 20)
    world.add_processor(movement_processor, 10)

    return world