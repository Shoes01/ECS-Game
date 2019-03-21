import esper
import numpy as np
import tcod as libtcod

from components.actor import Actor
from components.game.state import StateComponent
from components.player import Player
from components.position import Position
from components.render import Render
from components.tile import Tile
from components.turn import Turn
from components.velocity import Velocity
from processors.action import ActionProcessor
from processors.input import InputProcessor
from processors.level import LevelProcessor
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
    world.add_component(player, Actor())
    world.add_component(player, Player())
    world.add_component(player, Position(x=15, y=15))
    world.add_component(player, Render(char='@', color=libtcod.white))
    world.add_component(player, Turn())
    world.add_component(player, Velocity())

    fov_map = libtcod.map.Map(game_map.width, game_map.height, order='F')
    for ent, (pos, tile) in world.get_components(Position, Tile):
        fov_map.walkable[pos.x, pos.y] = not tile.blocks_path
        fov_map.transparent[pos.x, pos.y] = not tile.blocks_sight

    ############==================== The stuff above will eventually be moved into either a game starting processor, or it's own little game starting function.

    # Instantiate Processors.
    action_processor = ActionProcessor()
    prerender_processor = PrerenderProcessor(fov_map=fov_map)
    input_processor = InputProcessor()
    level_processor = LevelProcessor(tiles=game_map.tiles)
    movement_processor = MovementProcessor()
    render_processor = RenderProcessor(console=root)
    state_processor = StateProcessor()
    
    # Add them to the world.
    world.add_processor(level_processor, 999)
    world.add_processor(state_processor, 998)
    world.add_processor(prerender_processor, 110)
    world.add_processor(render_processor, 100)
    world.add_processor(input_processor, 99)
    world.add_processor(action_processor, 90)
    world.add_processor(movement_processor, 50)

    return world