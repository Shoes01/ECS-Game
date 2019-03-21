import esper
import numpy as np
import tcod as libtcod

from components.actor import Actor
from components.player import Player
from components.position import Position
from components.render import Render
from components.tile import Tile
from components.turn import Turn
from components.velocity import Velocity
from processors.action import ActionProcessor
from processors.input import InputProcessor
from processors.movement import MovementProcessor
from processors.prerender import PrerenderProcessor
from processors.render import RenderProcessor

def build_world(game_map, root):
    world = esper.World()

    # Create the player entity.
    player = world.create_entity()
    world.add_component(player, Actor())
    world.add_component(player, Player())
    world.add_component(player, Position(x=15, y=15))
    world.add_component(player, Render(char='@', color=libtcod.white))
    world.add_component(player, Turn())
    world.add_component(player, Velocity())

    # Create floor.
    for (x, y), _ in np.ndenumerate(game_map.tiles):
        if x == 17 and y == 17:
            wall = world.create_entity()
            world.add_component(wall, Position(x=x, y=y))
            world.add_component(wall, Render(char='#', color=libtcod.white, explored_color=libtcod.darkest_grey))
            world.add_component(wall, Tile())
        else:
            floor = world.create_entity()
            world.add_component(floor, Position(x=x, y=y))
            world.add_component(floor, Render(char='.', color=libtcod.white, explored_color=libtcod.darkest_grey))
            world.add_component(floor, Tile(False, False))

    fov_map = libtcod.map.Map(game_map.width, game_map.height, order='F')
    for ent, (pos, tile) in world.get_components(Position, Tile):
        fov_map.walkable[pos.x, pos.y] = not tile.blocks_path
        fov_map.transparent[pos.x, pos.y] = not tile.blocks_sight

    ############==================== The stuff above will eventually be moved into either a game starting processor, or it's own little game starting function.

    # Instantiate Processors.
    action_processor = ActionProcessor()
    prerender_processor = PrerenderProcessor(fov_map=fov_map)
    input_processor = InputProcessor()
    movement_processor = MovementProcessor()
    render_processor = RenderProcessor(console=root)
    
    # Add them to the world.
    world.add_processor(prerender_processor, 110)
    world.add_processor(render_processor, 100)
    world.add_processor(input_processor, 99)
    world.add_processor(action_processor, 90)
    world.add_processor(movement_processor, 50)

    return world