import esper
import tcod as libtcod

from components.player import Player
from components.position import Position
from components.render import Render
from components.turn import Turn
from components.velocity import Velocity
from processors.action import ActionProcessor
from processors.input import InputProcessor
from processors.movement import MovementProcessor
from processors.render import RenderProcessor

def build_world(root):
    world = esper.World()

    # Instantiate Processors.
    action_processor = ActionProcessor()
    input_processor = InputProcessor()
    movement_processor = MovementProcessor()
    render_processor = RenderProcessor(root)
    
    # Add them to the world.
    world.add_processor(render_processor, 100)
    world.add_processor(input_processor, 99)
    world.add_processor(action_processor, 90)
    world.add_processor(movement_processor, 50)

    # Create the player entity.
    player = world.create_entity()
    world.add_component(player, Player())
    world.add_component(player, Position(x=15, y=15))
    world.add_component(player, Render('@', libtcod.white))
    world.add_component(player, Turn())
    world.add_component(player, Velocity())

    return world